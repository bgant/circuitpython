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

import displayio
image_buffer = displayio.Group()

with open("/display-ruler.bmp", "rb") as f:
    pic = displayio.OnDiskBitmap(f)
    # CircuitPython 6 & 7 compatible
    t = displayio.TileGrid(
        pic, pixel_shader=getattr(pic, "pixel_shader", displayio.ColorConverter())
    )
    # CircuitPython 7 compatible only
    # t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
    image_buffer.append(t)

    display.show(image_buffer)

    display.refresh()

    print("drawing image...")

    while display.busy:
        pass  # Wait until all display processing is complete
