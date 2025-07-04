import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import serial
from photo import receive_photo
import threading

PORT = "COM15"
BAUDRATE = 115200

class PhotoApp:
    def __init__(self, master):
        self.master = master
        master.title("ESP32 Camera Viewer")

        self.ser = serial.Serial(PORT, BAUDRATE, timeout=1)

        self.label = ttk.Label(master, text="Last Captured Image:")
        self.label.pack(pady=5)

        self.image_label = tk.Label(master)
        self.image_label.pack(pady=10)

        self.capture_button = ttk.Button(master, text="📸 Take Picture", command=self.capture)
        self.capture_button.pack(pady=10)

    def capture(self):
        self.capture_button.config(state=tk.DISABLED)
        threading.Thread(target=self._capture_and_display).start()

    def _capture_and_display(self):
        try:
            self.ser.write(b'c')
            filename = receive_photo(self.ser)
            img = Image.open(filename)
            img.thumbnail((400, 300))
            photo = ImageTk.PhotoImage(img)

            self.image_label.config(image=photo)
            self.image_label.image = photo
        except Exception as e:
            print("❌ Error:", e)
        finally:
            self.capture_button.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = PhotoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
