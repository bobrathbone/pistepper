#!/usr/bin/env python3
#
# Raspberry Pi bipolar Stepper Motor test bipolar_class.py
# Author : Bob Rathbone
# $Id: control_nema17.py,v 1.4 2025/08/13 10:02:02 bob Exp $
# Site   : http://www.bobrathbone.com
#
# NEMA-17 bipolar stepper motor test 
# Example of controlling a Nema17 stepper motor with a rotary encoder and button interface
# Uses the A4988 H-bridge circuit driver board. 

import os,sys
import time
import atexit
from bipolar_lgpio_class import Motor
from rotary_class import RotaryEncoder

# NEMA-17 bipolar Motor BCM GPIO definitions
step = 21
direction = 20
enable = 25    
ms1 = 18
ms2 = 15
ms3 = 14

position = 1
button = None
revolution = 0

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

rotaryknob = RotaryEncoder(sia,sib,knob_switch, rotary_event)

motora = Motor(step,direction,enable,ms1,ms2,ms3)
motora.init()
motora.unlock()
revolution = motora.setStepSize(Motor.FULL)

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

