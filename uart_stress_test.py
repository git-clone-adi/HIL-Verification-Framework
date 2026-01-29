import serial
import time
import random
import os

# --- CONFIGURATION ---
SERIAL_PORT = 'COM3'  # Your Nucleo Port
BAUD_RATE = 115200
TEST_SIZE_BYTES = 10240  # 10KB of data
TIMEOUT_SEC = 5

def stress_test():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.5)
        print(f"Opened {SERIAL_PORT} at {BAUD_RATE} baud.")
    except Exception as e:
        print(f"FATAL: Could not open port. {e}")
        return

    # 1. Clear buffers
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    time.sleep(1)
    
    # Optional: Reset Nucleo
    ser.setDTR(False)
    time.sleep(0.1)
    ser.setDTR(True)
    time.sleep(2)

    # 2. Generate Random Data payload
    print(f"Generating {TEST_SIZE_BYTES} bytes of random data...")
    tx_data = os.urandom(TEST_SIZE_BYTES)
    
    # 3. The Blast
    print(">>> BLASTING DATA (Transmitting)...")
    start_time = time.perf_counter()
    
    bytes_written = ser.write(tx_data)
    print(f"Transmitted {bytes_written} bytes")
    
    # 4. The Catch
    print(">>> LISTENING (Receiving)...")
    rx_data = b''
    
    # Loop to read until we get all data or timeout
    loop_start = time.perf_counter()
    bytes_received = 0
    
    while len(rx_data) < TEST_SIZE_BYTES:
        if ser.in_waiting > 0:
            chunk = ser.read(ser.in_waiting)
            rx_data += chunk
            bytes_received += len(chunk)
            print(f"  Received: {bytes_received}/{TEST_SIZE_BYTES} bytes", end='\r')
        
        if (time.perf_counter() - loop_start) > TIMEOUT_SEC:
            print(f"\n\nTIMEOUT after {TIMEOUT_SEC} seconds.")
            break

    total_time = time.perf_counter() - start_time
    ser.close()

    # 5. The Autopsy
    print("\n\n--- RESULTS ---")
    print(f"Sent: {len(tx_data)} bytes")
    print(f"Recv: {len(rx_data)} bytes")
    print(f"Time: {total_time:.2f} seconds")
    
    if len(rx_data) != len(tx_data):
        lost_bytes = len(tx_data) - len(rx_data)
        print(f"\nFAIL: Data Packet Loss detected.")
        print(f"Lost {lost_bytes} bytes ({lost_bytes/TEST_SIZE_BYTES*100:.1f}%)")
        
        # Check first 100 bytes for corruption
        print("\nChecking first 100 bytes for corruption...")
        errors = 0
        for i in range(min(100, len(rx_data))):
            if tx_data[i] != rx_data[i]:
                errors += 1
                if errors == 1:
                    print(f"First mismatch at byte {i}: TX={hex(tx_data[i])} RX={hex(rx_data[i])}")
        if errors > 0:
            print(f"Total errors in first 100 bytes: {errors}")
        return

    if tx_data == rx_data:
        print("\n✅ PASS: 100% Integrity. Bit-perfect match.")
        throughput = (len(rx_data)*8)/total_time/1000
        print(f"Effective Throughput: {throughput:.2f} kbps")
        print(f"Data Rate: {len(rx_data)/total_time:.0f} bytes/sec")
    else:
        print("\n❌ FAIL: Data Corruption detected.")
        # Find first error
        for i in range(len(tx_data)):
            if tx_data[i] != rx_data[i]:
                print(f"First mismatch at byte index {i}: Sent {hex(tx_data[i])} received {hex(rx_data[i])}")
                break

if __name__ == "__main__":
    stress_test()