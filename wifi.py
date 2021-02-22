# Source: https://circuitpython.readthedocs.io/en/latest/shared-bindings/wifi/index.html

import wifi
from secrets import secrets

wifi.radio.connect(secrets['ssid'], secrets['password'])

wifi.radio.enabled
wifi.radio.ipv4_address
wifi.radio.ipv4_subnet
wifi.radio.ipv4_gateway
wifi.radio.ipv4_dns

wifi.radio.ap_info.ssid
wifi.radio.ap_info.channel
wifi.radio.ap_info.rssi      # Signal Strength
wifi.radio.ap_info.authmode
