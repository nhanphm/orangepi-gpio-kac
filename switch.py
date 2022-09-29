#!/usr/bin/env python3
import OPi.GPIO as GPIO # to install "pip3 install --upgrade OPi.GPIO"
import time
import subprocess
from server import sendSocket
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

#Select unused GPIO header pin to be used for shutdown
InputPin_1 = 13 #PA07/PA_EINT7/SIM_CLK
InputPin_2 = 15 #PA00/UART2_TX

# Set selected pin to input, need pullup resistor external in 3.3V and pin select.
GPIO.setup(InputPin_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(InputPin_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Set selected pin to output.

if GPIO.input(InputPin_1):
    print('Input was HIGH')
else:
    print('Input was LOW')

# Define a threaded callback function to run in another thread when events are detected  
def my_callback(channel):  
    if GPIO.input(channel):     # if port 25 == 1  
        print("Rising edge detected on ",channel)  
    else:                  # if port 25 != 1  
        print("Falling edge detected on", channel)  


# Wait for a button press on the selected pin (pin pulled to ground, falling edge)
#GPIO.wait_for_edge(InputPin, GPIO.BOTH)
STATE_ON = '1'
STATE_OFF = '0'
BUTTON_1 = '0'
BUTTON_2 = '1'

button_1_state=GPIO.PUD_UP
button_2 = True
button_2_state=GPIO.PUD_UP
while  True:
    if GPIO.input(InputPin_1) != button_1_state:
        button_1_state = GPIO.input(InputPin_1)
        print("Button 1 Switch")
        if GPIO.input(InputPin_1):     # if port 25 == 1  
            print("Buton 1 OFF")
            sendSocket(BUTTON_1, STATE_OFF)  
        else:                  # if port 25 != 1  
            print("Buton 1 ON")
            sendSocket(BUTTON_1, STATE_ON)
    
    if GPIO.input(InputPin_2) != button_2_state:
        button_2_state = GPIO.input(InputPin_2)
        print("Button 2 Switch")
        if GPIO.input(InputPin_2):     # if port 25 == 1  
            print("Buton 2 OFF")  
            sendSocket(BUTTON_2, STATE_OFF)
        else:                  # if port 25 != 1  
            print("Buton 2 ON")
            sendSocket(BUTTON_2, STATE_ON)

    time.sleep(1)

#GPIO.add_event_detect(InputPin, GPIO.BOTH, callback=my_callback(InputPin))  