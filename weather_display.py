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
# OpenWeatherMap images:
#    https://openweathermap.org/weather-conditions
#    Convert PNG image to BMP example:
#      * Open 01d@2x.png image in Gimp
#      * Set 'Paint Fill' to ABADB0 (Light Grey)
#      * Paint Fill the clear background 
#      * File --> Export As.. ---> 01.bmp --> Advanced Options --> 16 bits R5 G6 B5
#      * Copy 01.bmp image to CIRCUITPY/icons/
#
# Copy openweathermap.py  to CIRCUITPY/
# Copy weather_display.py to CIRCUITPY/code.py
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
DARK_GREY = 0x616163  # from panda_head.bmp test pattern
LIGHT_GREY = 0xABADB0  # from panda_head.bmp test pattern
WHITE = 0xFFFFFF

# Display Background Color
BACKGROUND = LIGHT_GREY


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
g = displayio.Group(max_size=20)

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
    text_group = displayio.Group(max_size=20, scale=scale, x=x, y=y)
    text_area = label.Label(FONT, text=text, color=color)
    text_group.append(text_area)  # Add this text to the text group
    g.append(text_group)
    #return (text_area.bounding_box[2], text_area.bounding_box[3])  # width, height of text block


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

    # Draw Icon Image
    icon = str(json_data['current']['weather'][0]['icon'])
    if '01d' in icon:
        icon = 'sun'
    elif '01n' in icon:
        icon = 'moon'
    else:
        icon = icon[:-1]  # Strip off the 'd' or 'n'
    #icon = '11'  # Test Options: sun moon 02 03 04 09 10 11 13 50
    image = "/icons/" + icon + ".bmp"
    draw_image(image=image, x=196, y=12)

    # Draw Current Temperature
    temp = str(round(json_data['current']['temp'])) + chr(176)
    print("Current Temp:", temp)
    draw_text(text=temp,scale=3,x=232,y=15,color=BLACK)

    # Draw "Feels Like" Temperature
    feels_like = str(round(json_data['current']['feels_like'])) + chr(176)
    draw_text(text='feels like',scale=1,x=214,y=97,color=BLACK)
    draw_text(text=feels_like,scale=2,x=234,y=112,color=BLACK)

    # Draw hourly forecast
    from time import localtime
    description_x = 37
    forecast_y = 23
    for i in range(0,5):
        hour_24 = localtime(json_data['hourly'][i]['dt'] + json_data['timezone_offset']).tm_hour 

        # Convert from 24-hour to 12-hour AM/PM format
        if hour_24 > 12:
            hour_12 = hour_24 - 12
        else:
            hour_12 = hour_24
        hour_string = str(hour_12) + str("PM" if hour_24 > 12 else "AM")

        # Line up hours on screen 
        if hour_12 > 9:
            hour_x = 4   # Adjust text to left 6 pixels (1 scale=1 character width) if 10, 11, or 12 to line up
        else:
            hour_x = 10

        # Draw Hour
        draw_text(text=hour_string,scale=1,x=hour_x,y=forecast_y,color=BLACK)

        # Draw Description
        description = str(json_data['hourly'][i]['weather'][0]['description'])
        #description = 'thunderstorm with heavy drizzle'  # Longest text string
        draw_text(text=description,scale=1,x=description_x,y=forecast_y,color=BLACK)
        
        # Shift down for next hourly forecast line
        forecast_y += 20

    # Push Image to the Display
    write_to_display()

    # Go to sleep
    import alarm
    from time import monotonic
    current_hour = localtime(json_data['current']['dt'] + json_data['timezone_offset']).tm_hour
    if current_hour > 11:
        time_alarm = alarm.time.TimeAlarm(monotonic_time=monotonic() + 25200) # Sleep until 6AM 
    else:
        time_alarm = alarm.time.TimeAlarm(monotonic_time=monotonic() + 600)   # Sleep 10 Minutes

except:
    print('ERROR')
    from time import sleep
    sleep(30)
    from microcontroller import reset
    reset()

finally: 
    displayio.release_displays() 
    spi.unlock()
    spi.deinit()  # Release IO36 SPI SCK Pin
    alarm.exit_and_deep_sleep_until_alarms(time_alarm)  # If USB is connected it says "Pretending to deep sleep until alerm, CTRL+C or file write"

