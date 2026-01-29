import serial
import time
import random
import os

SERIAL_PORT = 'COM3'
BAUD_RATE = 460800

def simple_echo_test():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1,
                           rtscts=False, dsrdtr=False)
        print(f"Opened {SERIAL_PORT} at {BAUD_RATE} baud.")
    except Exception as e:
        print(f"FATAL: Could not open port. {e}")
        return
    
    # Clear buffers
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    time.sleep(0.5)
    
    # 1. Send a simple test pattern first
    print("Sending test pattern 'ABCD'...")
    ser.write(b'ABCD')
    time.sleep(0.1)
    
    # Check for echo
    if ser.in_waiting > 0:
        echo = ser.read(ser.in_waiting)
        print(f"Received echo: {echo}")
    else:
        print("WARNING: No echo received!")
    
    # 2. Ask user to check physical connection
    print("\n--- HARDWARE CHECK ---")
    print("1. Ensure TX (PA2) is connected to RX (PA3) on Nucleo")
    print("2. Ensure Nucleo is programmed with echo firmware")
    print("3. Check baud rate in Nucleo code matches 460800")
    
    # 3. Small data test
    print("\n--- SMALL TEST (10 bytes) ---")
    test_data = b'TEST123456'
    print(f"Sending: {test_data}")
    ser.write(test_data)
    
    # Read with longer timeout
    rx_data = b''
    start = time.time()
    while len(rx_data) < len(test_data) and (time.time() - start) < 2:
        if ser.in_waiting > 0:
            rx_data += ser.read(ser.in_waiting)
    
    print(f"Received: {rx_data}")
    print(f"Bytes sent: {len(test_data)}, received: {len(rx_data)}")
    
    ser.close()

if __name__ == "__main__":
    simple_echo_test()