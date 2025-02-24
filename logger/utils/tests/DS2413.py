import time
import board
from adafruit_onewire.bus import OneWireBus
import adafruit_ds2413

ow_bus = OneWireBus(board.D2)
ds = adafruit_ds2413.DS2413(ow_bus, ow_bus.scan()[0])

led = ds.IOA
button = ds.IOB
button.direction = adafruit_ds2413.INPUT

while not button.value:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)