# Brandon Gant
# Created: 2021-02-24
# Updated:
#
# Unexpected Maker FeatherS2:
#     https://feathers2.io/
#     https://www.adafruit.com/product/4769
# Adafruit 2.9" E-Ink FeatherWing:
#     https://www.adafruit.com/product/4777
# CircuitPython 6.2:
#     https://circuitpython.org/board/unexpectedmaker_feathers2/
# CircuitPython Bundle Version 6.x Libraries:
#     https://circuitpython.org/libraries
#
# Libraries used by this script copied to CIRCUITPY/lib/
#     adafruit_il0373.mpy
#     adafruit_framebuf.mpy
#     adafruit_display_text/ 
#     adafruit_requests.mpy  <-- Used by openweathermap.py Module
#
# Create an /icons/ folder and populate it with OpenWeatherMap images:
#    https://openweathermap.org/weather-conditions
#
# Copy openweathermap.py to CIRCUITPY/
# Copy this weather_display.py script to CIRCUITPY/code.py
#

#----------------------------------------------------------------
# Display Settings
#----------------------------------------------------------------

# Board Specific Pins
from board import IO1,IO3,SCK,MOSI
EPD_CS = IO1  # FeatherS2 to 2.9" E-Ink FeatherWing ECS pin
EPD_DC = IO3  # FeatherS2 to 2.9" E-Ink FeatherWing DC pin

# Display Dimensions
DISPLAY_WIDTH  = 296
DISPLAY_HEIGHT = 128

# Display Colors
BLACK = 0x000000
DGREY = 0x616163  # from panda_head.bmp test pattern
LGREY = 0xABADB0  # from panda_head.bmp test pattern
WHITE = 0xFFFFFF

# Display Background Color
BACKGROUND = LGREY


#----------------------------------------------------------------
# Display Initialization
#----------------------------------------------------------------

import displayio

# Replease any display connections (just in case)
displayio.release_displays()

# Initialize SPI Display
from busio import SPI
spi = SPI(SCK, MOSI) 
display_bus = displayio.FourWire(
    spi, command=EPD_DC, chip_select=EPD_CS, baudrate=1000000
)

#from time import sleep
#sleep(1)  # Not sure why this was in original Adafruit example script

from adafruit_il0373 import IL0373
display = IL0373(
    display_bus,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    rotation=270,
    black_bits_inverted=False,
    color_bits_inverted=False,
    grayscale=True,
    refresh_time=1,
)

# Create a display group for our screen objects
g = displayio.Group(max_size=10)

# Set background color
background_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
palette = displayio.Palette(1)
palette[0] = BACKGROUND

# Create a Tilegrid with the background and put in the displayio group
t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
g.append(t)


#----------------------------------------------------------------
# Draw Text Function
#----------------------------------------------------------------

from terminalio import FONT
from adafruit_display_text import label
def draw_text(text="None", scale=2, x=20, y=40, color=BLACK):
    text_group = displayio.Group(max_size=10, scale=scale, x=x, y=y)
    text_area = label.Label(FONT, text=text, color=color)
    text_group.append(text_area)  # Add this text to the text group
    g.append(text_group)


#----------------------------------------------------------------
# Draw BMP Image Function
#----------------------------------------------------------------

def draw_image(image="/icons/10.bmp", x=0, y=0):
    f = open(image, "rb")  # 100x100 bitmap
    pic = displayio.OnDiskBitmap(f)
    t = displayio.TileGrid(pic, pixel_shader=displayio.ColorConverter(),x=x,y=y)
    g.append(t)


#----------------------------------------------------------------
# Write Text and Images on E-Ink Display
#----------------------------------------------------------------

def write_to_display():
    # Place the display group in the screen buffer
    display.show(g)

    # Refresh the Eink display to show the new screen
    display.refresh()

    while display.busy:
        pass  # Don't Exit script before screen refresh finishes


#----------------------------------------------------------------
# Main Code Block
#----------------------------------------------------------------
try:
    import openweathermap
    json_data = openweathermap.pull_data()
    feels_like = str(round(json_data['current']['feels_like'])) + chr(176) + 'F'
    print("Feels Like:",feels_like)
    draw_image(image="/icons/10.bmp", x=182, y=14)
    draw_text(text=feels_like,scale=3,x=20,y=20,color=BLACK)
    write_to_display()
finally: 
    displayio.release_displays() 
    spi.unlock()
    spi.deinit()  # Release IO36 SPI SCK Pin

