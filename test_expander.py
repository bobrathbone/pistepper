#!/usr/bin/env python3
#
# Raspberry Pi bipolar Stepper Motor test bipolar_class.py
# Author : Bob Rathbone
# $Id: test_expander.py,v 1.5 2025/09/18 08:58:42 bob Exp $
# Site   : http://www.bobrathbone.com
#
# NEMA-17 bipolar stepper motor test 
# Uses the A4988 H-bridge circuit driver board. 

import os
import sys 
import time
import atexit
from bipolar_lgpio_class import Motor

# NEMA-17 bipolar Motor BCM GPIO definitions
# Comment out the incorrect definition and un-comment the correct one 

# 26 pin header for older Raspberry Pi's            
"""
step = 24
direction = 4
enable = 25
ms1 = 23
ms2 = 22
ms3 = 27
"""

# 40 pin header for newer Raspberry Pi's            
step = 21
direction = 20
enable = 25     # Not required - leave unconnected
ms1 = 18
ms2 = 15
ms3 = 14

motora = Motor(step,direction,enable,ms1,ms2,ms3)
motora.init()
motora.reverse(False)   # Set to True to reverse motor polarity

print("Test expander board")
print("Motor GPIO settings")
print("  step",step)
print("  direction",direction)
print("  enable",enable)
print("Motor reversed",motora.isReversed())

# Get the number of steps per revoltion
# The step size must match the DIP switch setting on the expander board
revolution = motora.setStepSize(Motor.SIXTEENTH)
print("Revolution =", revolution)

print ("Motor A Clockwise sixteenth step")
motora.turn(revolution, Motor.CLOCKWISE)
time.sleep(1)

print ("Motor A Anticlockwise sixteenth step")
motora.turn(revolution, Motor.ANTICLOCKWISE)
time.sleep(1)

print ("Motor A goto", int(revolution/4))
motora.goto(int(revolution/4))
time.sleep(1)
motora.goto(1)

step = 12
count = 1
step = int(revolution/16)
x = range(16, revolution, step)
for pos in x:
    print("  %d Goto position %d" % (count,pos))
    motora.goto(pos)
    count += 1
    if count > 16:
        motora.stop()
        break
    time.sleep(0.5)

steps = motora.getPosition()
motora.turn(steps, Motor.ANTICLOCKWISE)

# Reset the motor otherwise it will become hot
motora.reset()
motora.unlock()
sys.exit(0)

# End of test program

# set tabstop=4 shiftwidth=4 expandtab
# retab

