#!/usr/bin/env python3
#
# Author : Bob Rathbone
# $Id: test_position.py,v 1.5 2023/05/23 09:39:34 bob Exp $
# Site   : http://www.bobrathbone.com
#
# Raspberry Pi Single Stepper Motor test positions
# Hardware 28BYJ-48 Stepper motor (Unipolar)

import os
import sys
import time
import atexit
from unipolar_class import Motor

# 24 pin header wiring
motora = Motor(17,18,27,22)
motorb = Motor(4,25,24,23)

motor = motora  # Select which motor you want to test
minute = 60

motor.init()

def finish():
	motor.stop()
	return

atexit.register(finish)

print ("1 rev", motor.REVOLUTION)
motor.lock()
print ("Position", motor.getPosition())

motor.turn(1*Motor.REVOLUTION, Motor.CLOCKWISE)
print ("Position", motor.getPosition())

time.sleep(2)
motor.goto(256)
print ("Position", motor.getPosition())
time.sleep(2)

motor.goto(128)
print ("Position", motor.getPosition())
time.sleep(2)

motor.goto(0)
print ("Position", motor.getPosition())
time.sleep(2)

motor.goto(384)
print ("Position", motor.getPosition())
time.sleep(2)

motor.goto(0)
print ("Position", motor.getPosition())
time.sleep(2)

motor.stop()

# End of program
