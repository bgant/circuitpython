'''
Raspberry Pi Pico W
https://www.adafruit.com/product/5526
https://www.sparkfun.com/products/20173
https://www.pishop.us/product/raspberry-pi-pico-w/

Example Pi Pico LED Usage:
from my_pi_pico_led import led
led(1) or led(True)
led(0) or led(False)
'''

import board
import digitalio

def led(state=0):
    if state:
        led = digitalio.DigitalInOut(board.LED)
        led.direction = digitalio.Direction.OUTPUT
        led.value = True
        led.deinit()
    else:
        led = digitalio.DigitalInOut(board.LED)
        led.direction = digitalio.Direction.OUTPUT
        led.value = False
        led.deinit()
