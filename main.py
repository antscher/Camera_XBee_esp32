# main.py

import serial
from photo import receive_photo

PORT = "COM15"       # Adapt according to your OS
BAUDRATE = 115200

def main():
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print(f"📡 Connected to {PORT} at {BAUDRATE} baud")

    while True:
        # Ask the user for a command
        cmd = input("📝 Type a command ('c' to capture, 'q' to quit): ").strip()
        if cmd == 'q':
            print("👋 Program ended")
            break
        elif cmd == 'c':
            ser.write(b'c')  # Send capture command to the device
            print("📤 Command 'c' sent")
            receive_photo(ser)  # Receive and save the photo
        else:
            print("❓ Unknown command")

    ser.close()  # Close the serial port

if __name__ == "__main__":
    main()