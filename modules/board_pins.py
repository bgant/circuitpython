# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Sources:
#    https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython-pins-and-modules
#    https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/CircuitPython_Essentials/Pin_Map_Script/code.py

"""CircuitPython Essentials Pin Map Script"""
import microcontroller
import board

board_pins = []
for pin in dir(microcontroller.pin):
    if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
        pins = []
        for alias in dir(board):
            if getattr(board, alias) is getattr(microcontroller.pin, pin):
                pins.append("board.{}".format(alias))
        if len(pins) > 0:
            board_pins.append(" ".join(pins))
for pins in sorted(board_pins):
    print(pins)
