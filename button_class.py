#!/usr/bin/env python3
# Raspberry Pi Button Push Button Class
# $Id: button_class.py,v 1.1 2025/08/16 06:50:54 bob Exp $
#
# Author: Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#            The authors shall not be liable for any loss or damage however caused.
#
#

import os,sys
import time
import RPi.GPIO as GPIO
import threading
import pdb

GPIO.setmode(GPIO.BCM)

# Up/Down constants (switch levels)

class Button:

    def __init__(self,button,callback,pull_up_down):
        t = threading.Thread(target=self._run,args=(button,callback,pull_up_down,))
        t.daemon = True
        t.start()

    def _run(self,button,callback,pull_up_down):
        self.button = button
        self.callback = callback
        self.pull_up_down = pull_up_down

        if self.button > 0:
            GPIO.setwarnings(False)

            if pull_up_down == GPIO.PUD_DOWN:
                edge = GPIO.RISING
                sEdge = 'Rising'
            elif  pull_up_down == GPIO.PUD_UP:
                edge = GPIO.FALLING
                sEdge = 'Falling'
            else:
                edge = GPIO.BOTH
                sEdge = 'Both'
            try:
                msg = "Creating button object for GPIO " +  str(self.button) \
                     + " edge=" +  sEdge
                print(msg)
                # The following lines enable the internal pull-up resistor
                GPIO.setup(self.button, GPIO.IN, pull_up_down=pull_up_down)

                # Add event detection to the GPIO inputs
                GPIO.add_event_detect(self.button, edge, 
                            callback=self.button_event,
                            bouncetime=200)
            except Exception as e:
                print("Button GPIO " + str(self.button)\
                         + " initialise error: " + str(e))
                sys.exit(1)
         
    # Push button event
    def button_event(self,button):
        #print("Push button event GPIO " + str(button))
        event_button = self.button
        self.callback(event_button) # Pass button event to event class
        return

    # Was a button pressed (goes from 0 to 1 or 1 to 0 depending upon pull_up_down )
    def pressed(self):
        level = 1
        if self.pull_up_down == GPIO.PUD_UP:
            level = 0
        state = GPIO.input(self.button)
        if state == level:
            bpressed = True
        else:
            bpressed = False
        return bpressed

# End of Button Class

### Test routine ###

def interrupt(gpio):
    print("Button pressed on GPIO", gpio)
    return

if __name__ == "__main__":

    print("Test Button Class")

    # Set up switch configuration
    motor_switch = 26
    print("Motor switch GPIO", motor_switch)

    Button(motor_switch, interrupt, GPIO.PUD_UP)

    try:
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print(" Stopped")
        GPIO.cleanup()
        sys.exit(0)

# End of script

# set tabstop=4 shiftwidth=4 expandtab
# retab

