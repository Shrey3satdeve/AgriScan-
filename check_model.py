import os
import numpy as np # type: ignore
import tensorflow as tf # type: ignore
from tensorflow.keras.preprocessing.image import load_img, img_to_array # type: ignore
import json
import random

MODEL_PATH = "model/agriscan_efficientnet.h5"
CLASS_NAMES_PATH = "model/class_names.json"
DATASET_DIR = "dataset/archive (1)/PlantVillage/PlantVillage"

def check_model():
    if not os.path.exists(MODEL_PATH):
        print(f"Model not found at {MODEL_PATH}")
        return

    print("Loading model...")
    model = tf.keras.models.load_model(MODEL_PATH)
    
    with open(CLASS_NAMES_PATH, "r") as f:
        class_names = json.load(f)
    class_names = {int(k): v for k, v in class_names.items()}

    # Pick 5 random classes
    all_classes = [d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))]
    sample_classes = random.sample(all_classes, min(5, len(all_classes)))

    print("\n--- Running Predictions ---")
    for cls in sample_classes:
        cls_dir = os.path.join(DATASET_DIR, cls)
        img_name = random.choice(os.listdir(cls_dir))
        img_path = os.path.join(cls_dir, img_name)
        
        # Load and preprocess
        img = load_img(img_path, target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Prediction
        preds = model.predict(img_array, verbose=0)[0]
        pred_idx = np.argmax(preds)
        pred_label = class_names.get(pred_idx, "Unknown")
        confidence = preds[pred_idx]
        
        print(f"Actual: {cls}")
        print(f"Predicted: {pred_label} ({confidence:.4f})")
        print("-" * 20)

if __name__ == "__main__":
    check_model()
