

'''secrets.py
secrets = {
    'ssid'        : '',
    'password'    : '',
    'timezone'    : 'America/Chicago',
    'lat'         : '',
    'lon'         : '',
    'appid'       : '<from https://api.openweathermap.org>',
    'server'      : '',
    'port'        : '',
    'database'    : '',
    'measurement' : '',
    'jwt'         : '<from https://jwt.io/#debugger-io>'
    }
'''

'''JSON Web Token (jwt)
If you enabled authentication in InfluxDB you need
to create a JSON Web Token to write to a database:

    https://www.unixtimestamp.com/index.php
        Create a future Unix Timestamp expiration   

    https://jwt.io/#debugger-io
        HEADER
            {
              "alg": "HS256",
              "typ": "JWT"
             }
        PAYLOAD
            {
              "username": "<InfluxDB username with WRITE to DATABASE>",
              "exp": <Unix Timestamp expiration>
            }
        VERIFY SIGNATURE
            HMACSHA256(
              base64UrlEncode(header) + "." +
              base64UrlEncode(payload),
              <shared secret phrase set in InfluxDB>
            )
'''

###################################
# Import Built-in Functions
###################################
import board
from time import sleep
import wifi
from displayio import Group
import ssl
import socketpool
import gc


###################################
# Import Library Bundle Functions
###################################
import adafruit_requests
import adafruit_ntp
# adafruit_bitmap_font
# adafruit_display_text
# adafruit_max31856
# adafruit_ssd1680


###################################
# Import Custom Functions
###################################
from my_adafruit_thermocouple import thermocouple
from my_adafruit_2in13_eInk import DISPLAY, DISPLAY_WIDTH, DISPLAY_HEIGHT
from my_image_functions import draw_background_color, draw_text, draw_image
from my_pi_pico_led import led
from my_client_id import client_id
try:
    from secrets import secrets
except:
    print('You need to create a secrets.py file... See example at the top of this script.')
led(0)

###################################
# Initialize Wifi
###################################
wifi.radio.connect(secrets["ssid"], secrets["password"])
pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=-5)


###################################
# Initialize HTTPS
###################################
https = adafruit_requests.Session(pool, ssl.create_default_context())
JSON_URL = "https://api.openweathermap.org/data/2.5/weather?lat=" + secrets['lat'] + "&lon=" + secrets['lon'] + "&units=imperial&appid=" + secrets['appid']


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
degree = '°'
#degree = str(chr(176)) # XML Decimal
#degree = b'\xC2\xB0'.decode() # utf-8
#degree = '\u00b0'  # utf-16


###################################
# Air Temperature Function
###################################
def air_reading():
    if 6 < ntp.datetime[3] < 23:  # Run between 7AM and 11PM to conserve API Calls
        response = https.get(JSON_URL)
        json_data = response.json()
        response.close()
        #print(json_data)
        feels_like = json_data['main']['feels_like']
        print(f'Air Feels Like: {int(roundTraditional(feels_like,0))}{degree}F')
        return feels_like
    else:
        print(f'Skip Night-time Air Reading to conserve API calls...')
        return None
    
# Account for size of 3-digit Air Temperatures
def air_digits(air):
    if air > 99:    # Number has 3 Digits
        return -10  # Move x-coordinate farther left on screen
    else:
        return 14   # Normal x-coordinate two-digit position

    

###################################
# Water Temperature Function
###################################
# Rounding the way you expect in Math
def roundTraditional(val,digits):
   return round(val+10**(-len(str(val))-1), digits)

def water_reading():
    thermoTempF = (sensor.temperature * 9.0/5.0) + 32
    print(f'Water Temp:     {int(roundTraditional(thermoTempF,0))}{degree}F')
    return thermoTempF


###################################
# InfluxDB Function
###################################
def send_to_influxdb(water):
    if '443' in secrets['port']:
        url = 'https://%s/influx/write?db=%s' % (secrets['server'], secrets['database'])
    else:
        url = 'http://%s:%s/write?db=%s' % (secrets['server'], secrets['port'], secrets['database'])
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Authorization': ''
    }
    headers['Authorization'] = 'Bearer %s' % secrets['jwt']
    data = "%s,device=%s water=%.1f" % (secrets['measurement'], client_id, water)
    response = https.post(url, headers=headers, data=data)
    if '204' in str(response.status_code):  # HTTP Status 204 (No Content) indicates server fulfilled request
        print(f'DB: {secrets['database']} \t Measurement: {data} \t Status: {response.status_code} Success')
    else:
        print(f'DB: {secrets['database']} \t Measurement: {data} \t Status: {response.status_code} Failed')


###################################
# Send Water Temp Alert to Pushover
###################################


###################################
# Main Function
###################################
last_air   = None
last_water = None

def main():
    gc.collect()
    print(f'Memory Free:   {int(gc.mem_free()/1024)}KB')
    
    # If Power Lost Change Display and Exit

    # Update Air and Water Readings
    water = water_reading()
    try:
        air = air_reading()
    except:
        air = None
    
    # Send Water Reading to InfluxDB
    send_to_influxdb(water)
    
    # Update Display Only if Readings have Changed
    air = None if air is None else int(roundTraditional(air,0))
    water = int(roundTraditional(water,0))
    global last_air
    global last_water
    if air == last_air and water == last_water:
        print('Readings have not changed / No Display Update')
        return  # Exit without continuing

    # Update Last Values before next Loop
    last_air   = air
    last_water = water

    # Create a display group for our screen objects
    image_buffer = Group()
    image_buffer.append(draw_background_color(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, color=0xffffff))
    image_buffer.append(draw_image('/pool.bmp', x=0, y=0))
    if air:
        image_buffer.append(draw_text(string=str(air), scale=1, x=air_digits(air), y=50, color=0x000000, font='/GothamBlack-54.bdf'))
        image_buffer.append(draw_text(string='Air', scale=1, x=40, y=95, color=0x000000, font='/GothamBlack-25.bdf'))
    image_buffer.append(draw_text(string=str(water), scale=1, x=14, y=185, color=0x000000, font='/GothamBlack-54.bdf'))
    image_buffer.append(draw_text(string='Water', scale=1, x=20, y=231, color=0x000000, font='/GothamBlack-25.bdf'))
    display.show(image_buffer)
    display.refresh()  # NOTE: Do not refresh eInk displays more often than 180 seconds!
    
    print('Drawing Image on Display...')
    while display.busy:
        pass  # Wait until all display processing is complete


###################################
# Main Running Loop
###################################
sleep_interval = 300  # Time between loops
while True:
    try:
        main()
        print(f'Sleeping for {sleep_interval} seconds...')
        print('')
        sleep(sleep_interval)
        while display.time_to_refresh > 0:  # Just in case sleep_interval is too short
            pass
    except Exception as e:
        print('ERROR:', e)
        print(f'Sleeping for {sleep_interval} seconds before Soft-Reset...')
        sleep(sleep_interval)
        from supervisor import reload
        reload()  # Soft-Reset

