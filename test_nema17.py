#!/usr/bin/env python3
#
# Raspberry Pi bipolar Stepper Motor test bipolar_class.py
# Author : Bob Rathbone
# $Id: test_nema17.py,v 1.7 2025/08/11 09:06:27 bob Exp $
# Site   : http://www.bobrathbone.com
#
# NEMA-17 bipolar stepper motor test 
# Uses the A4988 H-bridge circuit driver board. 

import os
import time
import atexit
from bipolar_lgpio_class import Motor
#from bipolar_class import Motor

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

# Reset the motor otherwise it will become hot
motora.reset()

# End of test program

# set tabstop=4 shiftwidth=4 expandtab
# retab

