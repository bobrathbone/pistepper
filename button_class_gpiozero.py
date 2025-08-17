#!/usr/bin/env python3
# Raspberry Pi Button Push Button Class using gpiozero interface
# $Id: button_class_gpiozero.py,v 1.2 2025/08/17 08:56:57 bob Exp $
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
import threading
import pdb
from gpiozero import Button

UP = 1
DOWN = 0

class ButtonClass:
    buttonobj = None

    def __init__(self,button,callback,pull_up_down):
        self.button = button
        self.callback = callback
        self.pull_up_down = pull_up_down

        t = threading.Thread(target=self._run,args=(button,callback,pull_up_down,))
        t.daemon = True
        t.start()

    def _run(self,button,callback,pull_up_down):
        self.button = button
        self.callback = callback
        self.pull_up_down = pull_up_down

        if self.button > 0:
            if pull_up_down == DOWN:
                pull_up = False
            else:
                pull_up = True
            try:
                # The following lines enable the internal pull-up resistor
                push_button = Button(self.button,bounce_time=0.01,pull_up=True)

                # Add event detection to the GPIO inputs
                push_button.when_pressed = self.button_down_event
                push_button.when_released = self.button_up_event

            except Exception as e:
                print("Button GPIO " + str(self.button)\
                         + " initialise error: " + str(e))
                sys.exit(1)
         
    # Button DOWN event
    def button_down_event(self,buttonobj):
        if self.buttonobj == None:
            self.buttonobj = buttonobj
        event = self.button
        self.callback(event)

    # Button UP event
    def button_up_event(self,buttonobj):
        if self.buttonobj == None:
            self.buttonobj = buttonobj
        event = self.button
        self.callback(event)

    # Was a button pressed (goes from 0 to 1 or 1 to 0 depending upon pull_up_down )
    def pressed(self):
        return self.buttonobj.is_pressed

# End of Button Class

### Test routine ###

if __name__ == "__main__":

    # Button events call this routine
    def button_event(gpio):
        print("Button pressed on GPIO", gpio)
        return

    pullupdown = ['DOWN','UP'] 

    print("Test Button Class")

    # Create button
    limit_switch = 26
    pull_up_down = ButtonClass.UP
    ButtonClass(limit_switch, button_event,pull_up_down)

    try:
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print(" Stopped")
        sys.exit(0)

# End of script

# set tabstop=4 shiftwidth=4 expandtab
# retab

