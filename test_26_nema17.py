#!/usr/bin/env python3
#
# Raspberry Pi Unipolar Stepper Motor test bipolar_class.py
# Author : Bob Rathbone
# $Id: test_26_nema17.py,v 1.3 2023/05/30 16:44:49 bob Exp $
# Site   : http://www.bobrathbone.com
#
# NEMA-17 unipolar stepper motor test 
# Uses the A4988 H-bridge circuit driver board. 

import os
import time
import atexit
from bipolar_class import Motor

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

def finish():
	motora.stop()
	return

atexit.register(finish)

# Get the number of steps per revoltion
count = 3
while count > 0:
	print ("Motor A Clockwise Full step")
	revolution = motora.setStepSize(Motor.FULL)
	motora.turn(revolution*3, Motor.CLOCKWISE)
	count -= 1
	time.sleep(1)

count = 3
while count > 0:
	print ("Motor A Anticlockwise Full step")
	revolution = motora.setStepSize(Motor.FULL)
	motora.turn(revolution*1, Motor.ANTICLOCKWISE)
	count -= 1
	time.sleep(1)

	print ("Motor A Clockwise Sixteenth step")
	revolution = motora.setStepSize(Motor.SIXTEENTH)
	motora.turn(revolution/2, Motor.CLOCKWISE)
	time.sleep(1)

revolution = motora.getRevolution()
print ("revolution = " + str(revolution))
print (str(motora.goto(revolution/4)))
time.sleep(2)
print (str(motora.goto((revolution/4)*3)))
time.sleep(2)
print (str(motora.goto(revolution/2)))
time.sleep(2)

# Reset motor otherwise it will become hot
motora.reset()

# End of program

# set tabstop=4 shiftwidth=4 expandtab
# retab
