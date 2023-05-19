
import board
from adafruit_2in13_eInk import DISPLAY, DISPLAY_WIDTH, DISPLAY_HEIGHT
display = DISPLAY(
    sck =   board.GP14,  # SPI1_SCK
    mosi =  board.GP15,  # SPI1_TX
    cs =    board.GP13,  # SPI1_CSn
    dc =    board.GP22,
    reset = board.GP27,
    busy =  board.GP26
    )

# Create a display group for our screen objects
import displayio
image_buffer = displayio.Group()

#################################################
# You can now use all Adafruit "display" examples
#################################################


# Source: https://learn.adafruit.com/quickstart-using-adafruit-eink-epaper-displays-with-circuitpython/example-simple-text

import terminalio
from adafruit_display_text import label

# Set a background
background_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
palette = displayio.Palette(1)  # Map colors in a palette
palette[0] = 0xff0000           # Background Color
background_color = displayio.TileGrid(background_bitmap, pixel_shader=palette)  # Create a Tilegrid with the background
image_buffer.append(background_color)

# Draw simple text using the built-in font into a displayio group
text_group = displayio.Group(scale=3, x=20, y=int(DISPLAY_HEIGHT/2))
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xffffff)
text_group.append(text_area)  # Add this text to the text group
image_buffer.append(text_group)

# Place the display group on the screen
display.show(image_buffer)

# Refresh the display to have everything show on the display
# NOTE: Do not refresh eInk displays more often than 180 seconds!
display.refresh()

print("drawing image...")

while display.busy:
    pass  # Wait until all display processing is complete
