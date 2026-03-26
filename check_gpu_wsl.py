import torch
import tensorflow as tf

print("--- PyTorch ---")
print(f"PyTorch GPU Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")

print("\n--- TensorFlow ---")
print(f"Num GPUs Available: {len(tf.config.list_physical_devices('GPU'))}")
print(tf.config.list_physical_devices('GPU'))

if len(tf.config.list_physical_devices('GPU')) == 0:
    print("\n[DIAGNOSTICS] TensorFlow couldn't find the GPU.")
    print("Checking for nvidia-cudnn in site-packages...")
    try:
        import nvidia.cudnn
        import os
        print(f"NVIDIA CUDNN found at: {os.path.dirname(nvidia.cudnn.__file__)}")
    except ImportError:
        print("NVIDIA CUDNN NOT FOUND in pip packages.")
