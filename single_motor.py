#!/usr/bin/env python
#
# Raspberry Pi Single Stepper Motor test motor_class.py
# Author : Bob Rathbone
# $Id: single_motor.py,v 1.2 2013/12/07 16:24:52 bob Exp $
# Site   : http://www.bobrathbone.com
#
import os
import time
import atexit
from motor_class import Motor

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
	print "Motor Clockwise"
	t1 = time.time()
	motor.turn(1*Motor.REVOLUTION, Motor.CLOCKWISE)
	t2 = time.time()
	print "time " + str(t2-t1)
	motor.lock()
	time.sleep(1)
	print "Motor  Anti-Clockwise"
	t1 = time.time()
	motor.turn(1*Motor.REVOLUTION, Motor.ANTICLOCKWISE)
	t2 = time.time()
	print "time " + str(t2-t1)
	motor.lock()
	time.sleep(5)
	if speed == motor.NORMAL:
		speed = motor.SLOW
	else:
		speed = motor.NORMAL
	motor.setSpeed(speed)	

# End of program
