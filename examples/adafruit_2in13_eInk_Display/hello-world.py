
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

# Create a display group for our screen objects
import displayio
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
text_area = label.Label(terminalio.FONT, text=text, color=RED)
text_group.append(text_area)  # Add this text to the text group
g.append(text_group)

# Place the display group on the screen
display.show(g)

# Refresh the display to have everything show on the display
# NOTE: Do not refresh eInk displays more often than 180 seconds!
display.refresh()

print("drawing image...")

while display.busy:
    pass  # Wait until all display processing is complete
