'''
Adafruit 2.13" Tri-Color eInk Display Breakout
https://www.adafruit.com/product/4947

Example Usage on Pi Pico:
import board
from my_adafruit_2in13_eInk import DISPLAY, DISPLAY_WIDTH, DISPLAY_HEIGHT
display = DISPLAY(
    sck    = board.GP14,  # SPI1_SCK
    mosi   = board.GP15,  # SPI1_TX
    cs     = board.GP13,  # SPI1_CSn
    dc     = board.GP22,
    reset  = board.GP27,
    busy   = board.GP26,
    enable = None
    )
'''

import board
from time import sleep
from busio import SPI
from displayio import release_displays, FourWire
import adafruit_ssd1680

DISPLAY_WIDTH  = 250
DISPLAY_HEIGHT = 122

BLACK = 0x000000
WHITE = 0xFFFFFF
RED =   0xFF0000

# Used to ensure the display is free in CircuitPython
release_displays()

def DISPLAY(sck=None, mosi=None, miso=None, cs=None, dc=None, reset=None, busy=None, enable=None):
    spi = SPI(sck, MOSI=mosi)  # Only uses SCK and MOSI
    display_bus = FourWire(spi, command=dc, chip_select=cs, reset=reset, baudrate=1000000)
    sleep(1)  # Wait a bit for the bus to initialize   
    # For issues with display not updating top/bottom rows correctly set colstart to 8
    return adafruit_ssd1680.SSD1680(
        display_bus,
        colstart = 8,
        width=DISPLAY_WIDTH,
        height=DISPLAY_HEIGHT,
        busy_pin=busy,
        highlight_color=RED,
        rotation=270,
        )
