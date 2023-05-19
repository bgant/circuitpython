''' Example Usage on Pi Pico:
import board
import adafruit_2in13_eInk
display = adafruit_2in13_eInk.DISPLAY(
    sck =   board.GP14,  # SPI1_SCK
    mosi =  board.GP15,  # SPI1_TX
    cs =    board.GP13,  # SPI1_CSn
    dc =    board.GP22,
    reset = board.GP27,
    busy =  board.GP26
    )
'''

import board
from time import sleep
from busio import SPI
from displayio import release_displays, FourWire
import adafruit_ssd1680

# Used to ensure the display is free in CircuitPython
release_displays()

def DISPLAY(sck=None, mosi=None, miso=None, cs=None, dc=None, reset=None, busy=None, enable=None):
    spi = SPI(sck, MOSI=mosi)  # Only uses SCK and MOSI
    display_bus = FourWire(spi, command=dc, chip_select=cs, reset=reset, baudrate=1000000)
    sleep(1)  # Wait a bit for the bus to initialize
    
    # Create the display object - the third color is red (0xff0000)
    # For issues with display not updating top/bottom rows correctly set colstart to 8
    return adafruit_ssd1680.SSD1680(
        display_bus,
        colstart=8,
        width=250,
        height=122,
        busy_pin=busy,
        highlight_color=0xFF0000,
        rotation=270,
        )
