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

