'''
Brandon Gant
Created: 2021-02-24
Updated: 2024-10-16

Unexpected Maker FeatherS2:
    https://feathers2.io/
    https://www.adafruit.com/product/4769
Adafruit 2.9" E-Ink FeatherWing:
    https://www.adafruit.com/product/4777
CircuitPython 6.2:
    https://circuitpython.org/board/unexpectedmaker_feathers2/
CircuitPython Bundle Version 6.x Libraries:
    https://circuitpython.org/libraries

Libraries used by this script copied to CIRCUITPY/lib/
    adafruit_il0373.mpy
    adafruit_framebuf.mpy
    adafruit_display_text/ 
    adafruit_requests.mpy

Convert PNG image to BMP example:
     * Open 01d@2x.png image in Gimp
     * Set 'Paint Fill' to ABADB0 (Light Grey)
     * Paint Fill the clear background 
     * File --> Export As.. ---> 01.bmp --> Advanced Options --> 16 bits R5 G6 B5
     * Copy 01.bmp image to CIRCUITPY/icons/

Copy weather_display.py to CIRCUITPY/code.py
'''

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
DARK_GREY = 0x616163   # from panda_head.bmp test pattern
LIGHT_GREY = 0xABADB0  # from panda_head.bmp test pattern
WHITE = 0xFFFFFF

# Display Background Color
BACKGROUND = LIGHT_GREY

# Forecast Block Location
forecast_location = {'x':5, 'y':23}

# Image and Temp Block Location
temp_location = {'x':202, 'y':12}


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
# Write Text and Images on E-Ink Display Function
#----------------------------------------------------------------

def write_to_display():
    # Place the display group in the screen buffer
    display.show(g)

    # Refresh the Eink display to show the new screen
    display.refresh()

    while display.busy:
        pass  # Don't Exit script before screen refresh finishes

#----------------------------------------------------------------
# Convert 24-hour time to 12-hour AM/PM Function
#----------------------------------------------------------------

def convert_hour(hour_24=12, forecast_x=4):
    if hour_24 is 0:
        hour_string = '12AM'
    elif hour_24 is 12:
        hour_string = '12PM'
    else:
        hour_string = str(hour_24 % 12) + str("PM" if hour_24 > 11 else "AM")
        if (hour_24 % 12) not in [10,11,12]:
            forecast_x += 6  # Line up single and double digit numbers
    return (hour_string, forecast_x)

#----------------------------------------------------------------
# Rounding like you learned in Math
#----------------------------------------------------------------

def roundTraditional(val,digits):
    '''Rounding like you learned in Math'''
    return round(val+10**(-len(str(val))-1), digits)


#----------------------------------------------------------------
# Main Code Block
#----------------------------------------------------------------

import ipaddress
import ssl
import wifi
import socketpool
import json
import adafruit_requests    # Copy adafruit_requests.mpy from Bundle to /lib/
try:
    from secrets import secrets # Create secrets.py file with key:value pairs (see note above)
except:
    print("You need to create a secrets.py file... See comments at the top of this script.")

try:
    wifi.radio.enabled = True
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    pool = socketpool.SocketPool(wifi.radio)
    
    ### Direct Request to OpenWeatherMap API
    #JSON_URL = "https://api.openweathermap.org/data/2.5/onecall?lat=" + secrets['lat'] + "&lon=" + secrets['lon'] + "&units=imperial&exclude=minutely&appid=" + secrets['appid']
    #https = adafruit_requests.Session(pool, ssl.create_default_context())
    #response = https.get(JSON_URL)
    #json_data = response.json()
    
    ### Request to local Webdis server
    URL = f'http://{secrets["webdis_host"]}:{secrets["webdis_port"]}/GET/{secrets["webdis_key"]}'
    http = adafruit_requests.Session(pool)
    response = http.get(URL)
    webdis_data = response.json()
    json_data = json.loads(webdis_data['GET'])  # Webdis adds a GET field at the beginning
    
    response.close()
    #wifi.radio.enabled = False  # Turning wifi off to conserve battery

    # Draw Icon Image
    icon_url = str(json_data['properties']['periods'][0]['icon'])  # URL string for icon
    #icon_url = "https://api.weather.gov/icons/land/night/tsra?size=small"  # Uncomment for testing
    icon_dict = {'02':['few','sct','wind_few','wind_sct'],  # Cloud with Sun
                  '04':['bkn','ovc','wind_bkn','wind_ovc'],  # Cloudy
                  '10':['rain_showers','rain_showers_hi'],   # Light Rain
                  '09':['rain','rain_snow','rain_sleet','fzra','rain_fzra','sleet','tropical_storm'],  # Rain
                  '13':['snow','show_sleet','snow_fzra','blizzard'],  # Snow
                  '11':['tsra','tsra_sct','tsra_hi'],        # Thunderstorm
                  '50':['dust','smoke','haze','fog'],        # Hard to see
                  }
    icon_image = None
    for image_number, weather in icon_dict.items():
        if icon_image:
            break
        icon_image = image_number if any(x in icon_url for x in weather) else None
    if not icon_image:
        icon_image = 'sun' if 'day' in icon_url else 'moon'
    #icon = '11'  # Test Options: sun moon 02 03 04 09 10 11 13 50
    image = "/icons/" + icon_image + ".bmp"
    draw_image(image=image, x=temp_location['x'], y=temp_location['y'])

    # Draw Current Temperature
    temp = str(round(json_data['properties']['periods'][0]['temperature'])) + chr(176)
    print("Current Temp:", temp)
    draw_text(text=temp,scale=3,x=temp_location['x'] + 36,y=temp_location['y'] + 3,color=BLACK)

    # Draw hourly forecast
    forecast_y = forecast_location['y']
    for i in range(0,5):
        # Draw Hour
        forecast_x = forecast_location['x']
        hour_24 = int(str(json_data['properties']['periods'][i]['startTime'])[11:-12:])
        hour_string, forecast_x = convert_hour(hour_24, forecast_x)   # Convert from 24-hour to 12-hour AM/PM format
        draw_text(text=hour_string,scale=1,x=forecast_x,y=forecast_y,color=BLACK)

        # Draw Description
        description = str(json_data['properties']['periods'][i]['shortForecast'])
        #description = 'thunderstorm with heavy drizzle'  # Longest text string
        draw_text(text=description,scale=1,x=forecast_location['x'] + 33,y=forecast_y,color=BLACK)
        
        # Shift down for next hourly forecast line
        forecast_y += 20
        
    # Draw "Feels Like" Temperature
    URL = f'http://{secrets["webdis_host"]}:{secrets["webdis_port"]}/GET/nws-feelslike'
    http = adafruit_requests.Session(pool)
    response = http.get(URL)
    webdis_data = response.json()
    json_data = json.loads(webdis_data['GET'])  # Webdis adds a GET field at the beginning
    response.close()
    #feels_like = str(json_data) + chr(176)
    feels_like = str(int(roundTraditional(float(json_data),0))) + chr(176)
    draw_text(text='feels like',scale=1,x=temp_location['x'] + 20,y=temp_location['y'] + 85,color=BLACK)
    draw_text(text=feels_like,scale=2,x=temp_location['x'] + 40,y=temp_location['y'] + 100,color=BLACK)

except Exception as e:
    print("ERROR", e)
    pass

# Push Image to the Display
write_to_display()

# Release all connections to Display
displayio.release_displays() 
spi.unlock()
spi.deinit()  # Release IO36 SPI SCK Pin

# Go into Deep Sleep
# Source: https://circuitpython.readthedocs.io/en/6.2.x/shared-bindings/alarm/index.html
import alarm
from time import monotonic
try:
    current_hour = localtime(json_data['current']['dt'] + json_data['timezone_offset']).tm_hour
    current_minute = localtime(json_data['current']['dt'] + json_data['timezone_offset']).tm_min
except:
    current_hour = 12
    current_minute = 0
#print("Current Time: %02d:%02d" % (current_hour,current_minute))
# Set the Deep Sleep Alarm
if current_hour > 24 or current_hour < 0:  # Effectively disabled since we are using Webdis now
    print("Setting Deep Sleep Alarm for 1 Hour")
    time_alarm = alarm.time.TimeAlarm(monotonic_time=monotonic() + 3600)  # Sleep 1 hour 
else:
    print("Setting Deep Sleep Alarm for 5 Minutes")
    time_alarm = alarm.time.TimeAlarm(monotonic_time=monotonic() + 300)   # Sleep 5 Minutes
# Deep sleep until the alarm goes off then restart the program
alarm.exit_and_deep_sleep_until_alarms(time_alarm)

