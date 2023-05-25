#!/usr/bin/env python3
#
# Raspberry Pi Single Stepper Motor test bipolar_class.py
# Author : Bob Rathbone
# $Id: single_motor.py,v 1.6 2023/05/23 09:33:11 bob Exp $
# Site   : http://www.bobrathbone.com
#
# Hardware 28BYJ-48 Stepper motor (Unipolar) - Single motor A test
# Motor driven  by a ULN2803A Eight Darlington outputs Driver Chip
# Uses the unipolar_class.py low level driver
#
import os
import time
import atexit
from unipolar_class import Motor

motor = Motor(17,18,27,22)
minute = 60

motor.init()

def finish():
	motor.stop()
	return

atexit.register(finish)

motor.lock()
time.sleep(2)
speed = motor.NORMAL

while True:
	print ("Motor Clockwise")
	t1 = time.time()
	motor.turn(1*Motor.REVOLUTION, Motor.CLOCKWISE)
	t2 = time.time()
	print ("time " + str(t2-t1))
	motor.lock()
	time.sleep(1)
	print ("Motor  Anti-Clockwise")
	t1 = time.time()
	motor.turn(1*Motor.REVOLUTION, Motor.ANTICLOCKWISE)
	t2 = time.time()
	print ("time " + str(t2-t1))
	motor.lock()
	time.sleep(5)
	if speed == motor.NORMAL:
		speed = motor.SLOW
	else:
		speed = motor.NORMAL
	motor.setSpeed(speed)	

# End of program
