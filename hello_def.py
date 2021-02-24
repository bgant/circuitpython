
import time

#----------------------------------------------------------------
# Display Settings
#----------------------------------------------------------------

# Board Specific Pins
import board
epd_cs = board.IO1  # FeatherS2 to 2.9" E-Ink FeatherWing ECS pin
epd_dc = board.IO3  # FeatherS2 to 2.9" E-Ink FeatherWing DC pin

# Display Dimensions
DISPLAY_WIDTH  = 296
DISPLAY_HEIGHT = 128

# Display Colors
BLACK = 0x000000
DGREY = 0x616163  # from panda_head.bmp test pattern
LGREY = 0xABADB0  # From panda_head.bmp test pattern
WHITE = 0xFFFFFF


#----------------------------------------------------------------
# Display Initialization
#----------------------------------------------------------------

import busio
import displayio
import terminalio
import adafruit_il0373
from adafruit_display_text import label

# Replease any display connections (just in case)
displayio.release_displays()

# Initialize SPI Display
spi = busio.SPI(board.SCK, board.MOSI)  # Uses SCK and MOSI
display_bus = displayio.FourWire(
    spi, command=epd_dc, chip_select=epd_cs, baudrate=1000000
)
time.sleep(1)

display = adafruit_il0373.IL0373(
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

# Map colors in a palette
palette = displayio.Palette(1)
palette[0] = WHITE

# Create a Tilegrid with the background and put in the displayio group
t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
g.append(t)


#----------------------------------------------------------------
# Text Function
#----------------------------------------------------------------

def draw_text(text="None", scale=2, x=20, y=40, color=BLACK):
    text_group = displayio.Group(max_size=10, scale=scale, x=x, y=y)
    text_area = label.Label(terminalio.FONT, text=text, color=color)
    text_group.append(text_area)  # Add this text to the text group
    g.append(text_group)


#----------------------------------------------------------------
# BMP Image Function
#----------------------------------------------------------------

def draw_image(image="/10d.bmp", x=0, y=0):
    f = open(image, "rb")  # 100x100 bitmap
    pic = displayio.OnDiskBitmap(f)
    t = displayio.TileGrid(pic, pixel_shader=displayio.ColorConverter(),x=x,y=y)
    g.append(t)


#----------------------------------------------------------------
# Display Text and Images on E-Ink Function 
#----------------------------------------------------------------

def write_to_display():
    # Place the display group on the screen
    display.show(g)

    # Refresh the Eink display to show the new screen
    display.refresh()

    while display.busy:
        pass


try:
    draw_text(text="more text",scale=2,x=45,y=70,color=LGREY)
    draw_text(text="testing",scale=1,x=70,y=100,color=DGREY)
    draw_image(image="/10d.bmp", x=182, y=14)
    write_to_display()
finally:
    displayio.release_displays()
    spi.unlock()
    spi.deinit()  # Release IO36 SCK Pin

