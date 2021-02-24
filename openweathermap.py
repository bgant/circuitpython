# Brandon Gant
# Created: 2021-02-21
# Updated: 2021-02-24
#
# Example secrets.py file:
#    secrets = {
#        'ssid'     : 'wifi_name',
#        'password' : 'wifi_password',
#        'lat'      : '40.0',           # Click on a spot in maps.google.com to see the Latitude and Longitude coordinates
#        'lon'      : '-88.0',
#        'appid'    : 'xxxxxxxxx',      # OpenWeatherMap.org AppID (sign up for free to get your own API Key)
#        }
#
# Example Usage:
#    import openweathermap
#    json_data = openweathermap.pull_data()
#    print(json_data['current']['temp']
#

# Function to connect to Wifi and pull down JSON data from OpenWeatherMap.org
def pull_data():
    import ipaddress
    import ssl
    import wifi
    import socketpool
    import adafruit_requests    # Copy adafruit_requests.mpy from Bundle to /lib/

    from secrets import secrets # Create secrets.py file with key:value pairs (see note above)
    JSON_URL = "https://api.openweathermap.org/data/2.5/onecall?lat=" + secrets['lat'] + "&lon=" + secrets['lon'] + "&units=imperial&exclude=minutely&appid=" + secrets['appid']
    wifi.radio.enabled = True
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    response = requests.get(JSON_URL)
    wifi.radio.enabled = False  # Turning wifi off to conserve battery
    return response.json()

