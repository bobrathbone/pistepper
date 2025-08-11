#!/usr/bin/env python3
#
# Raspberry Pi Unipolar Stepper Motor test bipolar_class.py
# Author : Bob Rathbone
# $Id: test_26_nema17.py,v 1.4 2025/08/09 11:13:04 bob Exp $
# Site   : http://www.bobrathbone.com
#
# NEMA-17 unipolar stepper motor test 
# Uses the A4988 H-bridge circuit driver board. 

import os
import time
import atexit

from bipolar_lgpio_class import Motor   # Uses LGPIO library
# This program can also be used with RPi GPIO. Comment out previous lie and uncomment next
#from bipolar_class import Motor    # Usses RPi.GPIO library

# NEMA-17 Unipolar Motor BCM GPIO definitions
# Comment out the incorrect definition and un-comment the correct one 

# GPIO assignments for 26-pin header for older Raspberry Pi's            
step = 24
direction = 4
enable = 25
ms1 = 23
ms2 = 22
ms3 = 27

# GPIO assignments for 40-pin header for newer Raspberry Pi's            
"""
step = 21
direction = 20
enable = 25     # Not required - leave unconnected
ms1 = 18
ms2 = 15
ms3 = 14
"""

motora = Motor(step,direction,enable,ms1,ms2,ms3)
motora.init()

# Get the number of steps per revoltion

print ("Motor A Clockwise Full step")
revolution = motora.setStepSize(Motor.FULL)
motora.turn(revolution*3, Motor.CLOCKWISE)
time.sleep(1)

print ("Motor A Anticlockwise Full step")
revolution = motora.setStepSize(Motor.FULL)
motora.turn(revolution*1, Motor.ANTICLOCKWISE)
time.sleep(1)

print ("Motor A Clockwise Sixteenth step")
revolution = motora.setStepSize(Motor.SIXTEENTH)
motora.turn(revolution/2, Motor.CLOCKWISE)
time.sleep(1)

revolution = motora.setStepSize(Motor.QUARTER)
revolution = motora.getRevolution()
print ("revolution = " + str(revolution))
print("Goto",int(revolution/4))
motora.goto(int(revolution/4))
time.sleep(1)
print("Goto",int(revolution*3/4))
motora.goto(int(revolution*3/4))
time.sleep(1)
print("Goto",int(revolution/2))
motora.goto(int(revolution/2))
time.sleep(1)

print ("Motor A go CLOCKWISE in 16 x 12 steps")
revolution = motora.setStepSize(Motor.FULL)
step = 12
count = 1
x = range(12, 200, step)
for pos in x:
    print("  %d Goto position %d" % (count,pos))
    motora.goto(pos)
    count += 1
    time.sleep(0.5)

print("Unlock motora")
motora.unlock()
time.sleep(4)
print("Lock motora")
motora.lock()
time.sleep(4)

# Reset motor otherwise it will become hot
motora.reset()
# Close the motor
motora.close()

# End of program

# set tabstop=4 shiftwidth=4 expandtab
# retab
