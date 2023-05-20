import board
from my_adafruit_2in13_eInk import DISPLAY, DISPLAY_WIDTH, DISPLAY_HEIGHT
display = DISPLAY(
    sck   = board.GP14,  # SPI1_SCK
    mosi  = board.GP15,  # SPI1_TX
    cs    = board.GP13,  # SPI1_CSn
    dc    = board.GP22,
    reset = board.GP27,
    busy  = board.GP26,
    )

# Rounding the way you expect in Math
def roundTraditional(val,digits):
   return round(val+10**(-len(str(val))-1), digits)

# Read thermocouple water temperature
from my_adafruit_thermocouple import thermocouple
sensor = thermocouple(sck=board.GP18, mosi=board.GP19, miso=board.GP16, cs=board.GP17)
sensor.averaging = 8
thermoTempF = (sensor.temperature * 9.0/5.0) + 32
print(f"Thermocouple Temp: {thermoTempF:.1f}°F")
water = int(roundTraditional(thermoTempF, 0))



air   = 79
# Account for size of 3-digit Air Temperatures
if air > 99:
    air_digits = -10
else:
    air_digits = 14


# Create a display group for our screen objects
from displayio import Group
from my_image_functions import draw_background_color, draw_text, draw_image
image_buffer = Group()
image_buffer.append(draw_background_color(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, color=0xffffff))
image_buffer.append(draw_image('/pool.bmp', x=0, y=0))
image_buffer.append(draw_text(string=str(air), scale=1, x=air_digits, y=50, color=0x000000, font="/GothamBlack-54.bdf"))
image_buffer.append(draw_text(string="Air", scale=1, x=40, y=95, color=0x000000, font="/GothamBlack-25.bdf"))
image_buffer.append(draw_text(string=str(water), scale=1, x=14, y=185, color=0x000000, font="/GothamBlack-54.bdf"))
image_buffer.append(draw_text(string="Water", scale=1, x=20, y=231, color=0x000000, font="/GothamBlack-25.bdf"))
display.show(image_buffer)
display.refresh()  # NOTE: Do not refresh eInk displays more often than 180 seconds!

print("drawing image...")
while display.busy:
    pass  # Wait until all display processing is complete