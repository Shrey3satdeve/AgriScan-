"""
AgriScan - Flask Web Application
Serves the crop disease detection model with GradCAM visualization.
Runs in Demo Mode automatically if TensorFlow is not installed or model not found.
"""

import os
import io
import json
import base64
import numpy as np # type: ignore
import cv2 # type: ignore
from PIL import Image # type: ignore
from flask import Flask, request, jsonify, send_from_directory # type: ignore
from disease_info import get_disease_info # type: ignore

try:
    import tensorflow as tf # type: ignore
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    tf = None
    print("[WARN] TensorFlow not installed. Running in Demo Mode.")

# ─── Configuration ────────────────────────────────────────────────────────────
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "agriscan_efficientnet.h5")
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, "class_names.json")
IMG_SIZE = 224
UPLOAD_FOLDER = "uploads"
CONFIDENCE_THRESHOLD = 0.50  # 50% minimum confidence for a "certain" result
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder="static", template_folder="templates")

# ─── Load Model ───────────────────────────────────────────────────────────────
print("[INFO] Loading AgriScan model...")
model = None
class_names = {}

def load_model_and_classes():
    global model, class_names
    if not TF_AVAILABLE:
        print("[INFO] TensorFlow not available. Running in Demo Mode.")
        return
    try:
        model = tf.keras.models.load_model(MODEL_PATH) # type: ignore
        with open(CLASS_NAMES_PATH, "r") as f:
            class_names = json.load(f)
        class_names = {int(k): v for k, v in class_names.items()}
        print(f"[INFO] Model loaded — {len(class_names)} classes identified.")
    except Exception as e:
        print(f"[WARN] Could not load model: {e}")
        print("[INFO] Running in DEMO mode with simulated predictions.")

load_model_and_classes()


# ─── GradCAM Utility ──────────────────────────────────────────────────────────
def compute_gradcam(model, img_array, class_index):
    """
    Computes a GradCAM heatmap for the given image and class index.
    Finds the last convolutional layer automatically.
    """
    # Find the last conv layer
    last_conv_layer = None
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D): # type: ignore
            last_conv_layer = layer.name
            break
        # Handle EfficientNet's sub-model
        if hasattr(layer, 'layers'):
            for sublayer in reversed(layer.layers):
                if isinstance(sublayer, tf.keras.layers.Conv2D): # type: ignore
                    last_conv_layer = sublayer.name
                    break
            if last_conv_layer:
                break

    if not last_conv_layer:
        return None

    try:
        # Build gradient model targeting the base model's last conv layer
        base_model = model.layers[1]  # EfficientNetB0 is the 2nd layer
        grad_model = tf.keras.models.Model( # type: ignore
            inputs=[model.inputs],
            outputs=[base_model.get_layer("top_activation").output, model.output]
        )

        with tf.GradientTape() as tape: # type: ignore
            conv_outputs, predictions = grad_model(img_array)
            loss = predictions[:, class_index]

        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2)) # type: ignore
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap) # type: ignore
        heatmap = tf.nn.relu(heatmap) # type: ignore
        heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8) # type: ignore
        return heatmap.numpy()
    except Exception as e:
        print(f"[WARN] GradCAM error: {e}")
        return None


def overlay_heatmap(original_img_pil, heatmap, alpha=0.45):
    """Overlay GradCAM heatmap on the original image."""
    orig = np.array(original_img_pil.resize((IMG_SIZE, IMG_SIZE)))
    heatmap_resized = cv2.resize(heatmap, (IMG_SIZE, IMG_SIZE))
    heatmap_uint8 = np.uint8(255 * heatmap_resized)
    heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    heatmap_rgb = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    superimposed = cv2.addWeighted(orig, 1 - alpha, heatmap_rgb, alpha, 0)
    return superimposed


def pil_to_base64(img_array):
    """Convert numpy image array to base64 string for JSON response."""
    pil_img = Image.fromarray(img_array.astype(np.uint8))
    buffer = io.BytesIO()
    pil_img.save(buffer, format="JPEG", quality=90)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def preprocess_image(pil_img):
    """Resize and normalize image for model input."""
    img = pil_img.resize((IMG_SIZE, IMG_SIZE)).convert("RGB")
    img_array = np.array(img)
    return np.expand_dims(img_array, axis=0).astype(np.float32)

# ─── Demo mode helpers ────────────────────────────────────────────────────────
DEMO_CLASSES = list(get_disease_info.__code__.co_consts) if False else [
    "Tomato___Late_blight",
    "Tomato___healthy",
    "Corn_(maize)___Common_rust_",
    "Apple___Apple_scab",
    "Potato___Early_blight",
    "Grape___Black_rot",
]

# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory("templates", "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        pil_img = Image.open(file.stream).convert("RGB")
        img_array = preprocess_image(pil_img)
        heatmap = None # Initialize

        if model is not None:
            # ── Real prediction ──────────────────────────────────────────────
            predictions = model.predict(img_array, verbose=0)[0]
            top5_indices = np.argsort(predictions)[::-1][:5]

            predicted_class_idx = int(top5_indices[0])
            predicted_class_name = class_names.get(predicted_class_idx, "Unknown")
            confidence = float(predictions[predicted_class_idx])

            # Threshold Check
            if confidence < CONFIDENCE_THRESHOLD:
                predicted_class_name = "UNCERTAIN"
            else:
                # Only compute GradCAM for certain predictions
                heatmap = compute_gradcam(model, img_array, predicted_class_idx)
            
            top5 = [
                {
                    "class": class_names.get(int(i), f"Class {i}"),
                    "display_name": get_disease_info(class_names.get(int(i), "")).get("display_name", ""),
                    "confidence": float(predictions[i])
                }
                for i in top5_indices
            ]
        else:
            # ── Demo / simulation mode ───────────────────────────────────────
            import random
            predicted_class_name = random.choice(DEMO_CLASSES)
            confidence = round(random.uniform(0.78, 0.97), 4) # type: ignore
            heatmap = None

            remaining = 1.0 - confidence
            others = [c for c in DEMO_CLASSES if c != predicted_class_name][:4] # type: ignore
            rand_confs = np.random.dirichlet(np.ones(len(others))).tolist()
            top5 = [{"class": predicted_class_name,
                      "display_name": get_disease_info(predicted_class_name).get("display_name", ""),
                      "confidence": confidence}]
            for c, rc in zip(others, rand_confs):
                top5.append({
                    "class": c,
                    "display_name": get_disease_info(c).get("display_name", ""),
                    "confidence": round(rc * remaining, 4)
                })

        # ── Build response ─────────────────────────────────────────────────
        disease_info = get_disease_info(predicted_class_name)

        # GradCAM overlay
        gradcam_b64 = None
        if heatmap is not None:
            overlay = overlay_heatmap(pil_img, heatmap)
            gradcam_b64 = pil_to_base64(overlay)

        # Original image resized
        orig_resized = np.array(pil_img.resize((IMG_SIZE, IMG_SIZE)))
        orig_b64 = pil_to_base64(orig_resized)

        return jsonify({
            "success": True,
            "predicted_class": predicted_class_name,
            "confidence": confidence,
            "disease_info": disease_info,
            "top5": top5,
            "original_image": orig_b64,
            "gradcam_image": gradcam_b64,
            "is_simulated": model is None or predicted_class_name == "UNCERTAIN"
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "model_loaded": model is not None,
        "num_classes": len(class_names) if class_names else 0
    })


if __name__ == "__main__":
    print("[INFO] Starting AgriScan server at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
