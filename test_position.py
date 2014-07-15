#!/usr/bin/env python
#
# Raspberry Pi Single Stepper Motor test motor_class.py
# Author : Bob Rathbone
# $Id: test_position.py,v 1.1 2013/12/08 17:53:02 bob Exp $
# Site   : http://www.bobrathbone.com
#
import os
import sys
import time
import atexit
from motor_class import Motor

motora = Motor(17,18,27,22)
motorb = Motor(4,25,24,23)

motor = motorb
minute = 60

motor.init()

def finish():
	motor.stop()
	return

atexit.register(finish)

print "1 rev", motor.REVOLUTION
motor.lock()
print "Position", motor.getPosition()

motor.turn(1*Motor.REVOLUTION, Motor.CLOCKWISE)
print "Position", motor.getPosition()

#sys.exit()

time.sleep(2)
motor.goto(256)
print "Position", motor.getPosition()
time.sleep(2)

motor.goto(128)
print "Position", motor.getPosition()
time.sleep(2)

motor.goto(0)
print "Position", motor.getPosition()
time.sleep(2)

motor.goto(384)
print "Position", motor.getPosition()
time.sleep(2)

motor.goto(0)
print "Position", motor.getPosition()
time.sleep(2)

motor.stop()

# End of program
