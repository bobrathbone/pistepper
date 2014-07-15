#!/usr/bin/env python
#
# Raspberry Pi Dual Stepper Motor test motor_class.py
# Author : Bob Rathbone
# $Id: test_motor_class.py,v 1.10 2014/01/04 16:26:15 bob Exp $
# Site   : http://www.bobrathbone.com
#
import os
import time
import atexit
from motor_class import Motor

motora = Motor(17,18,27,22)
motorb = Motor(4,25,24,23)
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
print str(motora.goto(900))
time.sleep(2)

speed = Motor.NORMAL

# Uncomment for setting step type
#motora.setHalfStepDrive()
#motora.setFullStepDrive()
#motora.setWaveDrive()

count = 20
while count > 0:
	print "Motor A Clockwise step"
	motora.turn(Motor.STEP, Motor.CLOCKWISE)
	count -= 1
	time.sleep(1)

count = 10
while count > 0:
	print "Motor A Anticlockwise step"
	motora.turn(Motor.STEP*2, Motor.ANTICLOCKWISE)
	count -= 1
	time.sleep(1)

while True:
	print "Motor A Clockwise"
	t1 = time.time()
	motora.turn(1*Motor.REVOLUTION, Motor.CLOCKWISE)
	t2 = time.time()
        print "time " + str(t2-t1)
	motora.lock()
	time.sleep(1)

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
