#!/usr/bin/env python
#
# Raspberry Pi Dual Stepper Motor test motor_ic2_class.py
# Author : Bob Rathbone
# $Id: test_motor_i2c_class.py,v 1.6 2014/03/01 10:38:23 bob Exp $
# Site   : http://www.bobrathbone.com
#

import os
import time
import atexit
from motor_i2c_class import Motor
address = 0x20 # I2C address of MCP23017

# Define the stepper motors
motora = Motor(address,Motor.MOTOR_A)
motorb = Motor(address,Motor.MOTOR_B)
minute = 60

motora.init()
motorb.init()

def finish():
	motora.stop()
	motorb.stop()
	return

atexit.register(finish)

motora.lock()
motorb.lock()

print "revolution = " + str(Motor.REVOLUTION)
print str(motora.goto(200))
time.sleep(2)
print str(motora.goto(100))
time.sleep(2)
print str(motora.goto(300))
time.sleep(2)

speed = Motor.NORMAL

# Uncomment required stepping type
#motora.setHalfStepDrive()
#motora.setFullStepDrive()
#motora.setWaveDrive()

while True:
	print "Motor A Clockwise"
	t1 = time.time()
	motora.turn(1*Motor.REVOLUTION, Motor.CLOCKWISE)
	t2 = time.time()
        print "time " + str(t2-t1)

	print "Motor A Anti-Clockwise"
	t1 = time.time()
	motora.turn(1*Motor.REVOLUTION, Motor.ANTICLOCKWISE)
	t2 = time.time()
        print "time " + str(t2-t1)
	motora.lock()
	time.sleep(1)

	print "Motor B Clockwise"
	t1 = time.time()
	motorb.turn(1*Motor.REVOLUTION, Motor.CLOCKWISE)
	t2 = time.time()
        print "time " + str(t2-t1)

	print "Motor B Anti-Clockwise"
	t1 = time.time()
	motorb.turn(1*Motor.REVOLUTION, Motor.ANTICLOCKWISE)
	t2 = time.time()
        print "time " + str(t2-t1)
	motorb.lock()
	time.sleep(5)

	if speed == Motor.NORMAL:
                speed = Motor.SLOW
        else:
                speed = Motor.NORMAL
        motora.setSpeed(speed)


# End of program
