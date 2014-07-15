#!/usr/bin/python
#
# Raspberry Pi H circuit Unipolar  Motor test driver
# Author : Bob Rathbone
# $Id: test_h.py,v 1.2 2014/02/28 17:13:59 bob Exp $
# Site   : http://www.bobrathbone.com
#
#

# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
import atexit


# Motor 1 pin out
direction=4
step=24
enable=25
pulse=0.0007
interval=0.0007

ms1 = 23
ms2 = 22
ms3 = 27

# Step resolution (The last column is the multiplier for one revolution)
FullStep = [0,0,0,1]
HalfStep = [1,0,0,2]
QuarterStep = [0,1,0,4]
EighthStep = [1,1,0,8]
SixteenthStep = [1,1,1,16]

# Direction and other definitions
CLOCKWISE = GPIO.LOW
ANTICLOCKWISE = GPIO.HIGH
ENABLE = GPIO.LOW
DISABLE = GPIO.HIGH
STEPS = 200

# Set pin directions
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup IO pins
def setup_pins():
	GPIO.setup(direction,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(step,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(enable,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(ms1,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(ms2,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(ms3,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN)
	return

# Disable all lines
def clear_lines():
        GPIO.output(direction,GPIO.LOW)
        GPIO.output(step,GPIO.LOW)
        GPIO.output(enable,DISABLE)
        GPIO.output(ms1,GPIO.LOW)
        GPIO.output(ms2,GPIO.LOW)
        GPIO.output(ms3,GPIO.LOW)
	return

# Set up stepper resolution
def setStepResolution(stepres):
	GPIO.output(ms1,stepres[0])
	GPIO.output(ms2,stepres[1])
	GPIO.output(ms3,stepres[2])
	oneRevolution = STEPS * stepres[3]
	return oneRevolution


# Register clear lines
atexit.register(clear_lines)
setup_pins()

# Main loop
while True:
	GPIO.output(direction,CLOCKWISE)
	GPIO.output(enable,ENABLE)
	oneRevolution = setStepResolution(FullStep)
	#oneRevolution = setStepResolution(HalfStep)
	#oneRevolution = setStepResolution(QuarterStep)
	#oneRevolution = setStepResolution(EighthStep)
	#oneRevolution = setStepResolution(SixteenthStep)

	count = oneRevolution * 1
	while count > 0:
		GPIO.output(step,GPIO.HIGH)
		time.sleep(pulse)
		GPIO.output(step,GPIO.LOW)
		time.sleep(interval)
		count -= 1
	
	GPIO.output(enable,DISABLE)
	time.sleep(3)
	GPIO.output(enable,ENABLE)
	GPIO.output(direction,ANTICLOCKWISE)

	count = oneRevolution * 1
	while count > 0:
		GPIO.output(step,GPIO.HIGH)
		time.sleep(pulse)
		GPIO.output(step,GPIO.LOW)
		time.sleep(interval)
		count -= 1
	
	GPIO.output(enable,DISABLE)
	time.sleep(3)

