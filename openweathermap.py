import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
from secrets import secrets
import time

JSON_URL = "https://api.openweathermap.org/data/2.5/onecall?lat=" + secrets['lat'] + "&lon=" + secrets['lon'] + "&units=imperial&exclude=minutely&appid=" + secrets['appid']

wifi.radio.connect(secrets["ssid"], secrets["password"])

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

response = requests.get(JSON_URL)
json_data = response.json()

dt = json_data['current']['dt']
timezone_offset = json_data['timezone_offset']
feels_like = json_data['current']['feels_like']
description = json_data['current']['weather'][0]['description']
icon = json_data['current']['weather'][0]['icon']

time.localtime(json_data['current']['dt'] + timezone_offset)
time.localtime(json_data['current']['dt'] + timezone_offset).tm_hour

for x in range(1,7):
    print(str(json_data['hourly'][x]['dt']) + "\t" + str(json_data['hourly'][x]['weather'][0]['description']))

str(time.localtime(dt + timezone_offset).tm_hour % 12) + str("PM" if time.localtime(dt + timezone_offset).tm_hour > 12 else "AM")

