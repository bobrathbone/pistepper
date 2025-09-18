#!/usr/bin/env python3
#
# Raspberry Pi bipolar Stepper Motor test bipolar_class.py
# Author : Bob Rathbone
# $Id: nema17_screen.py,v 1.6 2025/08/21 16:36:20 bob Exp $
# Site   : http://www.bobrathbone.com
#
# NEMA-17 bipolar stepper motor test 
# Example of controlling a Nema17 stepper motor with a rotary encoder and button interface
# Uses the A4988 H-bridge circuit driver board. 

import os,sys
import time
import atexit
import RPi.GPIO as GPIO
from time import strftime
from bipolar_lgpio_class import Motor
from rotary_class_gpiozero import RotaryEncoderClass
from button_class_gpiozero import ButtonClass
from luma_class import LUMA

dateformat = "%H:%M %d/%m/%Y"

# NEMA-17 bipolar Motor BCM GPIO definitions
step = 21
direction = 20  # Direction signal GPIO
enable = 25    
ms1 = 18
ms2 = 15
ms3 = 14

position = 1
button = None
counter = 1     # Counter 1 to 16
revolution = 0  # Number of steps in a revolution (Step size dependent)
halt = False    # Local flag to break out of any loop if running

Names = ['NO_EVENT', 'CLOCKWISE', 'ANTICLOCKWISE', 'BUTTON DOWN', 'BUTTON UP']

NORMAL=0
FLIP=2

LEDs = [
        "265 nm", "275 nm", "280 nm", "300 nm", "308 nm", "310 nm", "325 nm", "340 nm", 
        "365 nm", "375 nm", "385 nm", "395 nm", "395 nm", "405 nm", "554 nm", "565 nm"
       ]

# Rotary events call this routine
def rotary_event(event):
    global position,counter
    name = ''
    try:
        name = Names[event]
    except:
        name = 'ERROR'

    steps = 1
    revolution = motora.setStepSize(Motor.FULL)
    print("Rotary event ", event, name)
    if event == 1 :
        motora.turn(steps, Motor.CLOCKWISE)
        motora.setPosition(1)
        counter = 1
    elif  event == 2:
        motora.turn(steps, Motor.ANTICLOCKWISE)
        motora.setPosition(1)
        counter = 1
    elif  event == 3:   # Encoder button down
        motora.goto(position)
        position += 13
        counter += 1 
        if motora.getPosition() > 16*12: # Return to start
            motora.turn(revolution, Motor.ANTICLOCKWISE) 
            position = 1 
            counter = 1
            motora.goto(position)
    #print("Position", motora.getPosition())

def limit_event(event):
    global halt
    if limit_button.pressed():
        print("Limit switch event",event,"pressed")
        motora.stop()   # Stops the motor 
        halt = True     # The halt flag is used to exit any loops

def back_event(event):
    global position,counter
    if back_button.pressed():
        print("Back switch event",event,"pressed")
        position -= 13
        counter -= 1
        if position < 1:
            position = 1
            counter = 1
        motora.goto(position)

def interrupt():
    return

device = 'SH1106'
font_size = 12
font_name = "DejaVuSansMono.ttf"

display = LUMA()
# FLIP = Flip display verticaly, NORMAL = Don't flip
display.init(None,device_driver=device,font_name=font_name,font_size=font_size,rotation=NORMAL)
font = display.setFontSize(font_size)

display.clear()

# Display splash
dir = os.path.dirname(__file__)
display.drawSplash(dir + "/images/raspberrypi.png",2)

display.clear()
sDate = strftime(dateformat)
display.out(1,sDate,interrupt)
display.out(2,"Initialising LED",interrupt)
display.out(4,"Press CONFIRM",interrupt)
display.update()

print("Test Neva17 bipolar motor")
print("Motor GPIO settings")
print("  step",step)
print("  direction",direction)
print("  enable",enable)
print("  ms1",ms1)
print("  ms2",ms2)
print("  ms3",ms3)

knob_switch = 17 # Rotary encoder switch
### knob_switch = 8 # Rotary encoder switch
sia = 23    # Rotary encoder sia signal
sib = 24    # Rotary encoder sib signal
print("Rotary encoder")
print("  Rotary SIA signal GPIO", sia)
print("  Rotary SIB signal GPIO", sib)
print("  Rotary Knob button GPIO", knob_switch)
rotaryknob = RotaryEncoderClass(sia,sib,knob_switch,rotary_event)
 
limit_switch = 26
print("  Limit switch GPIO", limit_switch)
limit_button = ButtonClass(limit_switch,limit_event,GPIO.PUD_UP)

back_switch = 8
print("  Back switch GPIO", back_switch)
back_button = ButtonClass(back_switch,back_event,GPIO.PUD_UP)

motora = Motor(step,direction,enable,ms1,ms2,ms3)
motora.init()
motora.unlock()
revolution = motora.setStepSize(Motor.FULL)

count = 10
while count > 0:
    print ("Motor A Clockwise Sixteenth step")
    revolution = motora.setStepSize(Motor.SIXTEENTH)
    motora.turn(revolution, Motor.ANTICLOCKWISE)
    count -= 1
    if halt:
        motora.stop()
        halt = False
        break

display.out(2,"Set position 1",interrupt)
display.out(4,"Turn knob",interrupt)

motora.setDebug(False)  # Set to True for debug

try:
    while True:
        sDate = strftime(dateformat)
        display.out(1,sDate,interrupt)
        msg = "Position %d(%d)" % (counter,position)
        display.out(2,msg,interrupt)
        if counter < 17:
            idx = counter-1
            msg = "LED %d %s" % (counter,LEDs[idx])
            display.out(3, msg ,interrupt)
        display.out(4,"Press knob/BACK",interrupt)
        display.update()
        time.sleep(0.1)

except KeyboardInterrupt:
    print(" Stopped")
    motora.reset()
    sys.exit(0)

# Reset the motor otherwise it will become hot
motora.reset()

# End of test program

# set tabstop=4 shiftwidth=4 expandtab
# retab

