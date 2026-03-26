"""
AgriScan - Crop Disease Detection
Training Script using Transfer Learning with EfficientNetB0

Dataset: PlantVillage (subset via Kaggle or direct download)
Classes: 38 disease categories across multiple crops
"""

import os
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from pathlib import Path
import json
import tensorflow as tf # type: ignore
from tensorflow import keras # type: ignore
from tensorflow.keras import layers # type: ignore
from tensorflow.keras.applications import EfficientNetB0 # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore
from sklearn.metrics import classification_report, confusion_matrix # type: ignore
from sklearn.utils.class_weight import compute_class_weight # type: ignore
import warnings
warnings.filterwarnings('ignore')

# ─── Configuration ────────────────────────────────────────────────────────────
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS_WARMUP = 5      # Train only the head first
EPOCHS_FINETUNE = 15   # Then fine-tune the top layers
LEARNING_RATE_WARMUP = 1e-3
LEARNING_RATE_FINETUNE = 1e-4
DATASET_DIR = "dataset/archive (1)/PlantVillage/PlantVillage"   # corrected path
MODEL_DIR = "model"
HISTORY_FILE = "model/training_history.json"

# Check GPU at start
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"[INFO] Training on GPU: {gpus}")
else:
    print("[WARN] No GPU detected. TensorFlow on native Windows (>=2.11) requires WSL2 for GPU support.")

os.makedirs(MODEL_DIR, exist_ok=True)

# ─── Data Loading & Augmentation ──────────────────────────────────────────────
print("[INFO] Setting up data generators...")

train_datagen = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode="nearest",
    validation_split=0.2,
    preprocessing_function=tf.keras.applications.efficientnet.preprocess_input
)

val_datagen = ImageDataGenerator(
    validation_split=0.2,
    preprocessing_function=tf.keras.applications.efficientnet.preprocess_input
)

train_gen = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

val_gen = val_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

NUM_CLASSES = len(train_gen.class_indices)
print(f"[INFO] Found {NUM_CLASSES} classes: {list(train_gen.class_indices.keys())[:5]}...") # type: ignore

# Save class labels
class_names = {v: k for k, v in train_gen.class_indices.items()}
with open(os.path.join(MODEL_DIR, "class_names.json"), "w") as f:
    json.dump(class_names, f, indent=2)
print(f"[INFO] Class names saved to {MODEL_DIR}/class_names.json")

# Calculate Class Weights
print("[INFO] Calculating class weights...")
classes = train_gen.classes
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(classes),
    y=classes
)
class_weight_dict = {i: w for i, w in enumerate(class_weights)}
print(f"[INFO] Class weights: {class_weight_dict}")

# ─── Model Architecture ───────────────────────────────────────────────────────
print("[INFO] Building model with EfficientNetB0 backbone...")

base_model = EfficientNetB0(
    weights="imagenet",
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)
base_model.trainable = False  # Freeze backbone for warm-up

inputs = keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x = base_model(inputs, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.BatchNormalization()(x)
x = layers.Dense(512, activation="relu")(x)
x = layers.Dropout(0.4)(x)
x = layers.Dense(256, activation="relu")(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(NUM_CLASSES, activation="softmax")(x)

model = keras.Model(inputs, outputs)
model.summary()

# ─── Phase 1: Warm-up (train head only) ───────────────────────────────────────
print("\n[PHASE 1] Warm-up: Training classification head...")

model.compile(
    optimizer=keras.optimizers.Adam(LEARNING_RATE_WARMUP),
    loss="categorical_crossentropy",
    metrics=["accuracy", keras.metrics.TopKCategoricalAccuracy(k=5, name="top5_acc")]
)

callbacks_warmup = [
    keras.callbacks.ModelCheckpoint(
        os.path.join(MODEL_DIR, "best_model.h5"),
        monitor="val_loss",
        save_best_only=True,
        verbose=1
    ),
    keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, verbose=1),
    keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
]

history_warmup = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS_WARMUP,
    callbacks=callbacks_warmup,
    class_weight=class_weight_dict
)

# ─── Phase 2: Fine-tuning (unfreeze top layers) ───────────────────────────────
print("\n[PHASE 2] Fine-tuning top layers of EfficientNetB0...")

base_model.trainable = True
# Freeze all layers except the top 30
for layer in base_model.layers[:-30]:
    layer.trainable = False

model.compile(
    optimizer=keras.optimizers.Adam(LEARNING_RATE_FINETUNE),
    loss="categorical_crossentropy",
    metrics=["accuracy", keras.metrics.TopKCategoricalAccuracy(k=5, name="top5_acc")]
)

history_finetune = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS_FINETUNE,
    callbacks=callbacks_warmup,
    class_weight=class_weight_dict
)

# ─── Save Final Model ─────────────────────────────────────────────────────────
model.save(os.path.join(MODEL_DIR, "agriscan_efficientnet.h5"))
print(f"[INFO] Model saved to {MODEL_DIR}/agriscan_efficientnet.h5")

# ─── Plot Training History ────────────────────────────────────────────────────
all_acc = history_warmup.history["accuracy"] + history_finetune.history["accuracy"]
all_val_acc = history_warmup.history["val_accuracy"] + history_finetune.history["val_accuracy"]
all_loss = history_warmup.history["loss"] + history_finetune.history["loss"]
all_val_loss = history_warmup.history["val_loss"] + history_finetune.history["val_loss"]

# Save history
history_data = {
    "accuracy": all_acc,
    "val_accuracy": all_val_acc,
    "loss": all_loss,
    "val_loss": all_val_loss
}
with open(HISTORY_FILE, "w") as f:
    json.dump(history_data, f, indent=2)

fig, axs = plt.subplots(1, 2, figsize=(14, 5))
axs[0].plot(all_acc, label="Train Acc", color="#4CAF50")
axs[0].plot(all_val_acc, label="Val Acc", color="#2196F3", linestyle="--")
axs[0].axvline(x=EPOCHS_WARMUP, color="orange", linestyle=":", label="Fine-tune Start")
axs[0].set_title("Model Accuracy")
axs[0].set_xlabel("Epoch")
axs[0].legend()
axs[0].grid(True, alpha=0.3)

axs[1].plot(all_loss, label="Train Loss", color="#f44336")
axs[1].plot(all_val_loss, label="Val Loss", color="#9C27B0", linestyle="--")
axs[1].axvline(x=EPOCHS_WARMUP, color="orange", linestyle=":", label="Fine-tune Start")
axs[1].set_title("Model Loss")
axs[1].set_xlabel("Epoch")
axs[1].legend()
axs[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(MODEL_DIR, "training_history.png"), dpi=150)
plt.close()
print(f"[INFO] Training plot saved to {MODEL_DIR}/training_history.png")

# ─── Evaluation ───────────────────────────────────────────────────────────────
print("\n[INFO] Evaluating on validation set...")
val_gen.reset()
y_pred_probs = model.predict(val_gen, verbose=1)
y_pred = np.argmax(y_pred_probs, axis=1)
y_true = val_gen.classes

print("\n=== Classification Report ===")
target_names = [class_names[i] for i in range(NUM_CLASSES)]
report = classification_report(y_true, y_pred, target_names=target_names)
print(report)

with open(os.path.join(MODEL_DIR, "classification_report.txt"), "w") as f:
    f.write(report)

print("\n[SUCCESS] Training complete! All files saved in ./model/")
