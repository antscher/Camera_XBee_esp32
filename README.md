### ESP32 OV2640 Camera Image Transfer via XBee and Python
This project captures JPEG images on an ESP32 with an OV2640 camera and sends them over UART (XBee). A Python script triggers the capture and receives the image, saving it locally.

## Hardware Setup
- ESP32  freenove wrover with OV2640 camera module
- XBee connected to ESP32 UART2 (GPIO32 RX, GPIO33 TX)
- USB serial connection to PC (via XBee USB adapter)

## XBee Configuration with XCTU
To configure your XBee modules for communication with the ESP32 and your PC, use XCTU from Digi International.
a tutorial is here : https://circuitdigest.com/microcontroller-projects/arduino-xbee-module-interfacing-tutorial

# Steps to Set Up:
1) Download and install XCTU from the official Digi website. 

2) Connect your PC XBee module via a USB-to-serial adapter and open XCTU.

3) Click "Add devices", select the appropriate COM port, and press "Finish" to detect your XBee.

4) Go to the Configuration tab and ensure these settings:

- Baud Rate: 115200 (same as your ESP32)

- PAN ID: Use the same ID on both XBee modules (e.g., 1234)

- Destination Address High/Low: Match to the other XBee’s 64-bit address

- API Mode: Transparent Mode (AT) is recommended for basic serial bridging

5) Click "Write" to save configuration.

Make sure both XBee modules are on the same PAN and use the same baud rate (115200) for reliable communication. Avoid using 1152000 unless you’re sure both devices (and their adapters) support it, as most default UARTs can’t handle such high rates reliably.

## Arduino IDE Setup
Install Arduino IDE (1.8+).
Connect camera and XBee as per code pin definitions.
Select the board : "ESP32 wrover Module"
Upload the Arduino sketch with camera_sender.h.

## Python Environment Setup
Install pyserial for serial communication:
pip install pyserial

## How It Works
ESP32 waits for command 'c' on UART2.
On 'c', captures image and sends:
Start sequence (4 bytes)
Image size (4 bytes, big-endian)

JPEG data

End sequence (4 bytes)

Python script sends 'c' command and listens for image frames.
Image saved as image_recue_X.jpg with incrementing numbers.

## Usage
Run Python script:
python main.py

In terminal, type:

- 'c' + Enter — capture and receive image
- 'q' + Enter — quit program

Images saved in the script’s folder.

## Important
- Match baud rates (115200) and serial port name.
- Ensure hardware connections correspond to defined pins.
- Frame format ensures data integrity.