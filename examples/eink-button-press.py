import time
import board
import digitalio

A = digitalio.DigitalInOut(board.IO7)
A.direction = digitalio.Direction.INPUT
A.pull = digitalio.Pull.UP

B = digitalio.DigitalInOut(board.IO10)
B.direction = digitalio.Direction.INPUT
B.pull = digitalio.Pull.UP

C = digitalio.DigitalInOut(board.IO11)
C.direction = digitalio.Direction.INPUT
C.pull = digitalio.Pull.UP

while True:
    if not A.value:
        print("A button pressed")
        time.sleep(0.5)
    elif not B.value:
        print("B button pressed")
        time.sleep(0.5)
    elif not C.value:
        print("C button pressed")
        time.sleep(0.5)
    time.sleep(0.1)
