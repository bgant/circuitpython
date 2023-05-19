'''
Adafruit Universal Thermocouple Amplifier MAX31856 Breakout
https://www.adafruit.com/product/3263

Example Pi Pico Usage:
import board
from my_adafruit_thermocouple import thermocouple
sensor = thermocouple(sck=board.GP18, mosi=board.GP19, miso=board.GP16, cs=board.GP17)
sensor.averaging = 8
thermoTempF = (sensor.temperature * 9.0/5.0) + 32
print(f"Thermocouple Temp: {thermoTempF:.1f}°F")
'''

import board
from busio import SPI
from digitalio import DigitalInOut, Direction
from adafruit_max31856 import MAX31856

def thermocouple(sck=None, mosi=None, miso=None, cs=None):
    spi = SPI(sck, MOSI=mosi, MISO=miso)
    chip_select = DigitalInOut(cs)
    chip_select.direction = Direction.OUTPUT
    return MAX31856(spi,chip_select)

