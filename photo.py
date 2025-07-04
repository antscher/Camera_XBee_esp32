# photo.py

import struct
import time
import os

START_SEQ = b'\xDE\xAD\xBE\xEF'  # Start sequence for the image frame
END_SEQ   = b'\xFE\xED\xFA\xCE'  # End sequence for the image frame

SAVE_DIR = "."  # Current directory, or change to a subdirectory like "./images"

def get_next_image_index():
    # Find the next available index for saving the image
    i = 1
    while os.path.exists(os.path.join(SAVE_DIR, f"image_recue_{i}.jpg")):
        i += 1
    return i

def save_jpeg(frame_bytes):
    # Save the received JPEG bytes to a file
    index = get_next_image_index()
    filename = os.path.join(SAVE_DIR, f"image_recue_{index}.jpg")
    with open(filename, "wb") as f:
        f.write(frame_bytes)
    print(f"[+] Image saved: {filename}")

def receive_photo(ser):
    buffer = bytearray()
    print("⏳ Waiting for image frame...")

    while True:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            buffer.extend(data)

            while True:
                start_idx = buffer.find(START_SEQ)
                if start_idx == -1:
                    break

                # Not enough data to read the size yet
                if len(buffer) < start_idx + 8:
                    break

                size_bytes = buffer[start_idx + 4 : start_idx + 8]
                img_size = struct.unpack('>I', size_bytes)[0]

                img_start = start_idx + 8
                img_end = img_start + img_size

                # Wait until the full image and end sequence are received
                if len(buffer) < img_end + 4:
                    break

                if buffer[img_end : img_end + 4] != END_SEQ:
                    print("❌ Invalid frame end")
                    buffer = buffer[start_idx + 1:]
                    continue

                frame = buffer[img_start : img_end]

                print(f"\n✅ Image received ({img_size} bytes)")
                save_jpeg(frame)

                buffer = buffer[img_end + 4:]
                return  # Stop after receiving one image

        time.sleep(0.01)  # Avoid busy waiting
