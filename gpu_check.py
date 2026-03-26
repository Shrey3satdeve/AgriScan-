import tensorflow as tf
import time

print("--- GPU Verification ---")
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"Found {len(gpus)} GPU(s):")
    for gpu in gpus:
        print(f"  - {gpu}")
else:
    print("No GPU detected by TensorFlow.")

print("\n--- Speed Test (Matrix Multiplication) ---")
if gpus:
    # Test on GPU
    size = 4000
    with tf.device('/GPU:0'):
        a = tf.random.normal([size, size])
        b = tf.random.normal([size, size])
        
        # Warmup
        _ = tf.matmul(a, b)
        
        start = time.time()
        for _ in range(10):
            c = tf.matmul(a, b)
        end = time.time()
        print(f"GPU Time for 10 matmuls ({size}x{size}): {end - start:.4f} seconds")
else:
    print("Skipping GPU test (not available).")

# CPU benchmark for comparison
size_cpu = 1000 # smaller for CPU to avoid long wait
with tf.device('/CPU:0'):
    a = tf.random.normal([size_cpu, size_cpu])
    b = tf.random.normal([size_cpu, size_cpu])
    start = time.time()
    for _ in range(10):
        c = tf.matmul(a, b)
    end = time.time()
    print(f"CPU Time for 10 matmuls ({size_cpu}x{size_cpu}): {end - start:.4f} seconds")
