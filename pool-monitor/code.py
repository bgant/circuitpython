

###################################
# Import Built-in Functions
###################################
import board
from time import sleep
from displayio import Group


###################################
# Import Custom Functions
###################################
from my_adafruit_thermocouple import thermocouple
from my_adafruit_2in13_eInk import DISPLAY, DISPLAY_WIDTH, DISPLAY_HEIGHT
from my_image_functions import draw_background_color, draw_text, draw_image


###################################
# Initialize Wifi
###################################


###################################
# Initialize Display
###################################
display = DISPLAY(
    sck   = board.GP14,  # SPI1_SCK
    mosi  = board.GP15,  # SPI1_TX
    cs    = board.GP13,  # SPI1_CSn
    dc    = board.GP22,
    reset = board.GP27,
    busy  = board.GP26,
    )

###################################
# Initialize MAX31856 Thermocouple
###################################
sensor = thermocouple(sck=board.GP18, mosi=board.GP19, miso=board.GP16, cs=board.GP17)
sensor.averaging = 8


###################################
# Water Temperature Function
###################################

# Rounding the way you expect in Math
def roundTraditional(val,digits):
   return round(val+10**(-len(str(val))-1), digits)

def water_reading():
    thermoTempF = (sensor.temperature * 9.0/5.0) + 32
    print(f'Thermocouple Temp: {thermoTempF:.1f}°F')
    return int(roundTraditional(thermoTempF, 0))


###################################
# Air Temperature Function
###################################

def air_reading():
    return 79
    
# Account for size of 3-digit Air Temperatures
def air_digits(air=None):
    if air > 99:    # Number has 3 Digits
        return -10  # Move x-coordinate farther left on screen
    else:
        return 14   # Normal x-coordinate two-digit position


###################################
# Main Function
###################################

last_air = None
last_water = None

def main():
    # If Power Lost Change Display and Exit

    # Update Air and Water Readings
    water = water_reading()
    air = air_reading()
    
    # Send Water Reading to InfluxDB
    
    # Update Display Only if Readings have Changed
    global last_air
    global last_water
    if air == last_air and water == last_water:
        print('Readings have not changed... No Display Update...')
        return  # Exit without continuing

    # Create a display group for our screen objects
    image_buffer = Group()
    image_buffer.append(draw_background_color(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, color=0xffffff))
    image_buffer.append(draw_image('/pool.bmp', x=0, y=0))
    image_buffer.append(draw_text(string=str(air), scale=1, x=air_digits(air), y=50, color=0x000000, font='/GothamBlack-54.bdf'))
    image_buffer.append(draw_text(string='Air', scale=1, x=40, y=95, color=0x000000, font='/GothamBlack-25.bdf'))
    image_buffer.append(draw_text(string=str(water), scale=1, x=14, y=185, color=0x000000, font='/GothamBlack-54.bdf'))
    image_buffer.append(draw_text(string='Water', scale=1, x=20, y=231, color=0x000000, font='/GothamBlack-25.bdf'))
    display.show(image_buffer)
    display.refresh()  # NOTE: Do not refresh eInk displays more often than 180 seconds!
    
    print('Drawing Image on Display...')
    while display.busy:
        pass  # Wait until all display processing is complete
    
    # Update Last Values before next Loop
    last_air = air
    last_water = water


###################################
# Main Running Loop
###################################

sleep_interval = 120  # Time between loops

while True:
    try:
        main()
        print(f'Sleeping for {sleep_interval} seconds...')
        print('')
        sleep(sleep_interval)
    except Exception as error:
        print('ERROR:', error)
        print(f'Sleeping for {sleep_interval} seconds before Reset...')
        sleep(sleep_interval)
        from supervisor import reload
        reload() # Soft Reset
        #from microcontroller import reset
        #reset()  # Hard Rest
