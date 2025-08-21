#!/usr/bin/env python3
#
# Raspberry Pi bipolar Stepper Motor test bipolar_class.py
# Author : Bob Rathbone
# $Id: control_nema17.py,v 1.8 2025/08/18 07:52:00 bob Exp $
# Site   : http://www.bobrathbone.com
#
# NEMA-17 bipolar stepper motor test 
# Example of controlling a Nema17 stepper motor with a rotary encoder and button interface
# Uses the A4988 H-bridge circuit driver board. 

import os,sys
import time
import atexit
import RPi.GPIO as GPIO
from bipolar_lgpio_class import Motor
from rotary_class_gpiozero import RotaryEncoderClass
from button_class_gpiozero import ButtonClass

# NEMA-17 bipolar Motor BCM GPIO definitions
step = 21
direction = 20  # Direction signal GPIO
enable = 25    
ms1 = 18
ms2 = 15
ms3 = 14

position = 1
button = None
revolution = 0  # Number of steps in a revolution (Step size dependent)
halt = False    # Local flag to break out of any loop if running

Names = ['NO_EVENT', 'CLOCKWISE', 'ANTICLOCKWISE', 'BUTTON DOWN', 'BUTTON UP']

# Rotary events call this routine
def rotary_event(event):
    global position
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
    elif  event == 2:
        motora.turn(steps, Motor.ANTICLOCKWISE)
        motora.setPosition(1)
    elif  event == 3:
        if position == 1:
            position += 12
        motora.goto(position)
        position += 12
        if motora.getPosition() > 16*12: # Return to start
            position = 1 
            motora.turn(revolution, Motor.ANTICLOCKWISE) 
            motora.goto(position)
    #print("Position", motora.getPosition())

def limit_event(event):
    global halt
    if limit_button.pressed():
        print("Limit switch event",event,"pressed")
        motora.stop()   # Stops the motor 
        halt = True     # The halt flag is used to exit any loops

print("Test Neva17 bipolar motor")
print("Motor GPIO settings")
print("  step",step)
print("  direction",direction)
print("  enable",enable)
print("  ms1",ms1)
print("  ms2",ms2)
print("  ms3",ms3)

knob_switch = 17 # Rotary encoder switch
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

motora.setDebug(False)  # Set to True for debug

try:
    while True:
        time.sleep(0.2)

except KeyboardInterrupt:
    print(" Stopped")
    motora.reset()
    sys.exit(0)

# Reset the motor otherwise it will become hot
motora.reset()

# End of test program

# set tabstop=4 shiftwidth=4 expandtab
# retab

