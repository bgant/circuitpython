'''Example Usage:
from my_client_id import client_id
'''

import wifi
wifi_dump = [hex(i) for i in wifi.radio.mac_address]
mac_list = [i[2:] for i in wifi_dump]
client_id = 'x' + ''.join(mac_list)