# Go to https://pypi.org/project/adafruit-circuitpython-hid
#   Click Download Files
#   Click *.tar.gz file to download and open
#   Extract adafruit_hid folder to CIRCUITPY/lib folder

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
