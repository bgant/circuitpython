
import board
from my_adafruit_2in13_eInk import DISPLAY, DISPLAY_WIDTH, DISPLAY_HEIGHT
display = DISPLAY(
    sck   = board.GP14,  # SPI1_SCK
    mosi  = board.GP15,  # SPI1_TX
    cs    = board.GP13,  # SPI1_CSn
    dc    = board.GP22,
    reset = board.GP27,
    busy  = board.GP26
    )

# Create a display group for our screen objects
from displayio import Group
from my_image_functions import draw_background_color, draw_text, draw_image
image_buffer = Group()
image_buffer.append(draw_background_color(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, color=0xff0000))
#image_buffer.append(draw_image('/display-ruler.bmp', x=20, y=20))
image_buffer.append(draw_text(string="Hello World!", scale=3, x=20, y=int(DISPLAY_HEIGHT/2), color=0x000000))
image_buffer.append(draw_text(string="Hello Again...", scale=1, x=20, y=90, color=0xffffff, font="/Comic-Bold-18.bdf"))
display.show(image_buffer)
display.refresh()  # NOTE: Do not refresh eInk displays more often than 180 seconds!

print("drawing image...")
while display.busy:
    pass  # Wait until all display processing is complete
