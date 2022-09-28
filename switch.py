#!/usr/bin/env python3
import OPi.GPIO as GPIO # to install "pip3 install --upgrade OPi.GPIO"
import time
import subprocess
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

#Select unused GPIO header pin to be used for shutdown
InputPin = 12 #PA07/PA_EINT7/SIM_CLK
LedOnPin = 13 #PA00/UART2_TX

# Set selected pin to input, need pullup resistor external in 3.3V and pin select.
GPIO.setup(InputPin, GPIO.IN)
# Set selected pin to output.
GPIO.setup(LedOnPin, GPIO.OUT)

GPIO.output(LedOnPin, 1)
if GPIO.input(InputPin):
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
GPIO.add_event_detect(InputPin, GPIO.BOTH, callback=my_callback(InputPin))   
    

#GPIO.add_event_detect(InputPin, GPIO.BOTH, callback=my_callback(InputPin))  