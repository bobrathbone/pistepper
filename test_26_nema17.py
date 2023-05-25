#!/usr/bin/env python3
#
# Raspberry Pi Unipolar Stepper Motor test bipolar_class.py
# Author : Bob Rathbone
# $Id: test_26_nema17.py,v 1.1 2023/05/24 11:14:37 bob Exp $
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

# 26 pin header for older Raspberry Pi's            
step = 24
direction = 4
enable = 25
ms1 = 23
ms2 = 22
ms3 = 27

# 40 pin header for newer Raspberry Pi's            
"""
step = 20
direction = 21
enable = 25	# Not used - backward compatability only
ms1 = 14
ms2 = 15
ms3 = 18
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

# End of program