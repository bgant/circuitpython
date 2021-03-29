# Go to https://github.com/adafruit/Adafruit_CircuitPython_HID
#   Click Code -> Download ZIP
#   Open .zip file and extract adafruit_hid folder to CIRCUITPY/lib folder

from time import sleep
import usb_hid
from adafruit_hid.mouse import Mouse

mouse = Mouse(usb_hid.devices)

def move_mouse():
    mouse.move(x=5,y=5)
    sleep(0.2)
    mouse.move(x=-5,y=-5)
    sleep(0.2)

while True:
     move_mouse()
     sleep(180)
