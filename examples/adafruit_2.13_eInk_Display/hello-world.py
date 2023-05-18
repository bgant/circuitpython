import time
import board
import busio
import displayio
import adafruit_ssd1680

displayio.release_displays()

# Using SPI1 on Pi Pico W
spi = busio.SPI(board.GP14, MOSI=board.GP15)  # Uses SCK and MOSI
epd_cs = board.GP13
epd_dc = board.GP22
epd_reset = board.GP27  # Set to None for FeatherWing
epd_busy = board.GP26  # Set to None for FeatherWing

display_bus = displayio.FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)
time.sleep(1)  # Wait a bit

# Create the display object - the third color is red (0xff0000)
# For issues with display not updating top/bottom rows correctly set colstart to 8
display = adafruit_ssd1680.SSD1680(
    display_bus,
    colstart=8,
    width=250,
    height=122,
    busy_pin=epd_busy,
    highlight_color=0xFF0000,
    rotation=270,
)

# Create a display group for our screen objects
g = displayio.Group()

#################################################
# You can now use all Adafruit "display" examples
#################################################


# Source: https://learn.adafruit.com/quickstart-using-adafruit-eink-epaper-displays-with-circuitpython/example-simple-text

import terminalio
from adafruit_display_text import label

DISPLAY_WIDTH = 250
DISPLAY_HEIGHT = 122

BLACK = 0x000000
WHITE = 0xFFFFFF
RED =   0xFF0000

FOREGROUND_COLOR = RED
BACKGROUND_COLOR = WHITE

# Set a background
background_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
# Map colors in a palette
palette = displayio.Palette(1)
palette[0] = BACKGROUND_COLOR

# Create a Tilegrid with the background and put in the displayio group
t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
g.append(t)

# Draw simple text using the built-in font into a displayio group
text_group = displayio.Group(scale=2, x=20, y=40)
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=BLACK)
text_group.append(text_area)  # Add this text to the text group
g.append(text_group)

# Place the display group on the screen
display.show(g)

# Refresh the display to have everything show on the display
# NOTE: Do not refresh eInk displays more often than 180 seconds!
display.refresh()

time.sleep(120)

while True:
    pass

