#!/usr/bin/env python
#
# Raspberry Pi Bipolar Stepper Motor test motor_class.py
# Author : Bob Rathbone
# $Id: test_bipolar_class.py,v 1.1 2014/03/04 11:57:53 bob Exp $
# Site   : http://www.bobrathbone.com
#
import os
import time
import atexit
from bipolar_class import Motor

# Bipolar Motor BCM GPIO definitions
direction = 04
enable = 25
step = 24
ms1 = 23
ms2 = 22
ms3 = 27

motora = Motor(step,direction,enable,ms1,ms2,ms3)
motora.init()

def finish():
	motora.stop()
	return

atexit.register(finish)

# Get the number of steps per revoltion
count = 3
while count > 0:
	print "Motor A Clockwise Full step"
	revolution = motora.setStepSize(Motor.FULL)
	motora.turn(revolution*3, Motor.CLOCKWISE)
	count -= 1
	time.sleep(1)

count = 3
while count > 0:
	print "Motor A Anticlockwise Full step"
	revolution = motora.setStepSize(Motor.FULL)
	motora.turn(revolution*1, Motor.ANTICLOCKWISE)
	count -= 1
	time.sleep(1)

	print "Motor A Clockwise Sixteenth step"
	revolution = motora.setStepSize(Motor.SIXTEENTH)
	motora.turn(revolution/2, Motor.CLOCKWISE)
	time.sleep(1)

revolution = motora.getRevolution()
print "revolution = " + str(revolution)
print str(motora.goto(revolution/4))
time.sleep(2)
print str(motora.goto((revolution/4)*3))
time.sleep(2)
print str(motora.goto(revolution/2))
time.sleep(2)

# End of program
