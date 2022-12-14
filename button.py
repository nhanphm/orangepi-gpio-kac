"""Read button.
Make gpio input and enable pull-up resistor.
"""

import os
import sys

if not os.getegid() == 0:
    sys.exit('Script must be run as root')


from pyA20.gpio import gpio
from pyA20.gpio import connector
from pyA20.gpio import port

button = connector.gpio3p40

"""Init gpio module"""
gpio.init()

"""Set directions"""
gpio.setcfg(button, gpio.INPUT)

"""Enable pullup resistor"""
gpio.pullup(button, gpio.PULLUP)
#gpio.pullup(button, gpio.PULLDOWN)     # Optionally you can use pull-down resistor

try:
    print ("Press CTRL+C to exit")
    while True:
        state = gpio.input(button)      # Read button state

        """Since we use pull-up the logic will be inverted"""
        print ("Button Status:", state)

except KeyboardInterrupt:
    print ("Goodbye.")