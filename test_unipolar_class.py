#!/usr/bin/env python3
#
# Raspberry Pi Dual Stepper Motor test bipolar_class.py
# Author : Bob Rathbone
# $Id: test_unipolar_class.py,v 1.6 2023/05/23 09:30:19 bob Exp $
# Site   : http://www.bobrathbone.com
#
# Hardware 28BYJ-48 Stepper motor (unipolar) - Dual motor A and B test
# Motor driven  by a ULN2803A Eight Darlington outputs Driver Chip
# Uses the unipolar_class.py low level driver

import os
import time
import atexit
from unipolar_class import Motor

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

print ("revolution = " + str(Motor.REVOLUTION))
print (str(motora.goto(200)))
time.sleep(2)
print (str(motora.goto(100)))
time.sleep(2)
print (str(motora.goto(900)))
time.sleep(2)

speed = Motor.NORMAL

# Uncomment for setting step type
#motora.setHalfStepDrive()
#motora.setFullStepDrive()
#motora.setWaveDrive()

count = 30
while count > 0:
    print ("Motor A Clockwise step")
    motora.turn(Motor.STEP, Motor.CLOCKWISE)
    count -= 1
    time.sleep(0.1)

count = 30
while count > 0:
    print ("Motor A Anticlockwise step")
    motora.turn(Motor.STEP*2, Motor.ANTICLOCKWISE)
    count -= 1
    time.sleep(0.1)

while True:
    print ("Motor A Clockwise")
    t1 = time.time()
    motora.turn(1*Motor.REVOLUTION, Motor.CLOCKWISE)
    t2 = time.time()
    print ("time " + str(t2-t1))
    motora.lock()
    time.sleep(1)

    print ("Motor A Anti-Clockwise")
    t1 = time.time()
    motora.turn(1*Motor.REVOLUTION, Motor.ANTICLOCKWISE)
    t2 = time.time()
    print ("time " + str(t2-t1))
    motora.lock()
    time.sleep(1)

    print ("Motor B Clockwise")
    t1 = time.time()
    motorb.turn(1*Motor.REVOLUTION, Motor.CLOCKWISE)
    t2 = time.time()
    print ("time " + str(t2-t1))

    print ("Motor B Anti-Clockwise")
    t1 = time.time()
    motorb.turn(1*Motor.REVOLUTION, Motor.ANTICLOCKWISE)
    t2 = time.time()
    print ("time " + str(t2-t1))
    motorb.lock()
    time.sleep(5)

    if speed == Motor.NORMAL:
        speed = Motor.SLOW
    else:
        speed = Motor.NORMAL
    motora.setSpeed(speed)


# End of program
