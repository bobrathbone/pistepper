#!/usr/bin/python
#
# Raspberry Pi Dual Stepper Motor test driver
# Author : Bob Rathbone
# $Id: test_stepper.py,v 1.1 2013/12/06 11:27:52 bob Exp $
# Site   : http://www.bobrathbone.com
#
# Based on code from ModMyPi
# https://www.modmypi.com/step-your-pi
#

# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
import atexit


# Motor 1 pin out
pin1=17
pin2=18
pin3=27
pin4=22

# Motor 2 pin out
pin5=23
pin6=24
pin7=25
pin8=4

# Set up for Motor 1
pinA = pin1
pinB = pin2
pinC = pin3
pinD = pin4

# set pin directions
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Highest torque speed
Apin1=[1,1,0,0,1]        
Apin2=[0,1,1,0,0]
Apin3=[0,0,1,1,0]
Apin4=[0,0,0,1,1]

# Lowest torque speed
#Apin1=[0,0,0,0,1]        
#Apin2=[0,0,0,1,0]
#Apin3=[0,0,1,0,0]
#Apin4=[0,1,0,0,0]

current=0	# Current position
target=0	# Target position
speed = 0.003
isMotorA = True

# Reset all pins
def setup_pins():
	GPIO.setup(pin1,GPIO.OUT)
	GPIO.setup(pin2,GPIO.OUT)
	GPIO.setup(pin3,GPIO.OUT)
	GPIO.setup(pin4,GPIO.OUT)
	GPIO.setup(pin5,GPIO.OUT)
	GPIO.setup(pin6,GPIO.OUT)
	GPIO.setup(pin7,GPIO.OUT)
	GPIO.setup(pin8,GPIO.OUT)
	return

def clear_lines():
	GPIO.output(pin1,GPIO.LOW)
	GPIO.output(pin2,GPIO.LOW)
	GPIO.output(pin3,GPIO.LOW)
	GPIO.output(pin4,GPIO.LOW)
	GPIO.output(pin5,GPIO.LOW)
	GPIO.output(pin6,GPIO.LOW)
	GPIO.output(pin7,GPIO.LOW)
	GPIO.output(pin8,GPIO.LOW)
	return

# Switch to motor A
def motor_A():
 	global pinA,pinB,pinC,pinD
	pinA = pin1
	pinB = pin2
	pinC = pin3
	pinD = pin4
	return

# Switch to motor B
def motor_B():
 	global pinA,pinB,pinC,pinD
	pinA = pin5
	pinB = pin6
	pinC = pin7
	pinD = pin8
	return


def position(target,current):
 #print current,target
 if current<target:
	 while current<target:
		 i=current&2 + 1
		 GPIO.output(pinA,Apin1[i])
		 GPIO.output(pinB,Apin2[i])
		 GPIO.output(pinC,Apin3[i])
		 GPIO.output(pinD,Apin4[i])
		 time.sleep(speed)
		 current= current + 1
 else:
	 while current>target:
		 i=current&2 + 1
		 GPIO.output(pinA,Apin1[i])
		 GPIO.output(pinB,Apin2[i])
		 GPIO.output(pinC,Apin3[i])
		 GPIO.output(pinD,Apin4[i])
		 #time.sleep(.003)
		 time.sleep(speed)
		 current= current - 1
 clear_lines()
 #print current,target
 return current;


#setup
setup_pins()
atexit.register(clear_lines)

motor_A()

while True:
	if isMotorA:
		print "Motor A"
	else:
		print "Motor B"

	target=3000
	current=position(target,current)

	time.sleep(2)
	target=200
	current=position(target,current)

	target=2000
	current=position(target,current)

	target=200
	current=position(target,current)
	time.sleep(2)

	if isMotorA:
		motor_B()
		isMotorA = False
	else:
		motor_A()
		isMotorA = True

