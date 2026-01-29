import time
import numpy as np

TARGET_HZ = 100
INTERVAL = 1.0 / TARGET_HZ
TEST_DURATION_SEC = 10

print(f"Testing PC Timer Stability for {TARGET_HZ}Hz stream...")

deltas = []
start_global = time.perf_counter()
next_wake = start_global + INTERVAL

while time.perf_counter() - start_global < TEST_DURATION_SEC:
    now = time.perf_counter()
    
    # Busy-wait loop for higher precision than time.sleep()
    while now < next_wake:
        now = time.perf_counter()
    
    # Record actual time vs expected time
    actual_delta = now - (next_wake - INTERVAL)
    deltas.append(actual_delta)
    
    next_wake += INTERVAL

# Analysis
deltas = np.array(deltas) * 1000 # Convert to ms
mean_dt = np.mean(deltas)
std_dev = np.std(deltas)
max_jit = np.max(deltas) - np.min(deltas)

print(f"\n--- RESULTS (Target: {INTERVAL*1000:.2f} ms) ---")
print(f"Mean Interval: {mean_dt:.4f} ms")
print(f"Standard Deviation: {std_dev:.4f} ms")
print(f"Max Jitter: {max_jit:.4f} ms")

if std_dev > 1.0:
    print(">>> FAIL: Your PC jitter is too high (>1ms). Do not proceed.")
    print(">>> FIX: Close heavy apps or increase thread priority.")
else:
    print(">>> PASS: Clock source is stable enough for HIL simulation.")