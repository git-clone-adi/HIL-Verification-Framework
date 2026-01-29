import serial
import time

# CHANGE THIS TO YOUR COM PORT
COM_PORT = 'COM3'  # Change to your port (COM5, COM6, etc.)
BAUD_RATE = 115200

print(f"Testing UART on {COM_PORT} at {BAUD_RATE} baud")
print("=" * 50)

try:
    # Open serial port
    ser = serial.Serial(
        port=COM_PORT,
        baudrate=BAUD_RATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=2,
        xonxoff=False,
        rtscts=False
    )
    
    print("✓ Serial port opened")
    
    # Clear buffers
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    
    # Send test character
    print("\n1. Sending single character 'A'")
    ser.write(b'A')
    time.sleep(0.1)
    
    # Check for echo
    if ser.in_waiting > 0:
        response = ser.read(ser.in_waiting)
        print(f"   Received: {response}")
        if response == b'A':
            print("   ✓ UART Echo WORKING!")
        else:
            print(f"   ✗ Got wrong echo: {response}")
    else:
        print("   ✗ No response received")
    
    # Test string
    print("\n2. Sending string 'HELLO'")
    ser.write(b'HELLO')
    time.sleep(0.2)
    
    if ser.in_waiting > 0:
        response = ser.read(ser.in_waiting)
        print(f"   Received: {response}")
    else:
        print("   ✗ No response")
    
    # Test with Enter key
    print("\n3. Testing with Enter key (\\r\\n)")
    ser.write(b'TEST\r\n')
    time.sleep(0.3)
    
    if ser.in_waiting > 0:
        response = ser.read(ser.in_waiting)
        print(f"   Received: {response}")
    else:
        print("   ✗ No response")
    
    ser.close()
    print("\nTest complete!")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    print("\nTroubleshooting:")
    print("1. Check COM port number in Device Manager")
    print("2. Ensure Nucleo is connected via USB")
    print("3. Try restarting Nucleo (press black RESET button)")
    print("4. Try different baud rate (115200)")