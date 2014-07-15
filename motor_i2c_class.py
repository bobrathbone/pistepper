#!/usr/bin/env python
#
# $Id: motor_i2c_class.py,v 1.5 2014/01/04 16:26:15 bob Exp $
# Raspberry Pi Stepper Motor Driver Class (I2C)
# Hardware 28BYJ-48 Stepper 
# Gear Reduction Ratio: 1/64 
# Step Torque Angle: 5.625 degrees /64
# 360/5.625 = 64
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com

import sys
import os
import time
import smbus

# The stepper motor can be driven in different ways
# See http://en.wikipedia.org/wiki/Stepper_motor

# Output pattern
out1=[]
out2=[]
out3=[]
out4=[]

# Full step drive (Maximum Torque)
Aout1=[1,1,0,0]
Aout2=[0,1,1,0]
Aout3=[0,0,1,1]
Aout4=[1,0,0,1]

# Wave drive (increase angular resolution)
Bout1=[1,0,0,0]
Bout2=[0,1,0,0]
Bout3=[0,0,1,0]
Bout4=[0,0,0,1]

# Half step drive ( Maximum angle minimum torque)
Cout1=[1,1,0,0,0,0,0,1]
Cout2=[0,1,1,1,0,0,0,0]
Cout3=[0,0,0,1,1,1,0,0]
Cout4=[0,0,0,0,0,1,1,1]

bus = smbus.SMBus(1)

class Motor:

	# Addressing
	address = 0x20 # I2C address of MCP23017
	BANK_A = 0
	BANK_B = 1
	MOTOR_A = 0
	MOTOR_B = 1
	MOTOR_C = 2
	MOTOR_D = 3

	CLOCKWISE = 0
	ANTICLOCKWISE = 1
	GEARING = 64
	STEPS = 8
	REVOLUTION = GEARING * STEPS
	NORMAL = 0.0027
	SLOW = NORMAL * 2
	running = False 
	position = 0
	halt = False

	def __init__(self,address,motor):
		self.address = address
		if  motor == self.MOTOR_B or motor == self.MOTOR_D:
			self.pin1 = 16
			self.pin2 = 32
			self.pin3 = 64
			self.pin4 = 128
		else:
			self.pin1 = 1
			self.pin2 = 2
			self.pin3 = 4
			self.pin4 = 8

		if  motor == self.MOTOR_C or motor == self.MOTOR_D:
			self.bank = self.BANK_B
		else:
			self.bank = self.BANK_A

		self.speed = self.NORMAL
		self.moving = False
		self.setFullStepDrive()
		return

	# Initialise 
	def init(self):
		if self.bank == self.BANK_A:
			bus.write_byte_data(0x20,0x00,0x00) # Set all of bank A to outputs
		else:
			bus.write_byte_data(0x20,0x01,0x00) # Set all of bank B to outputs
		self.zeroPosition()
		return	

	# Reset (stop) motor
	def reset(self):
		self.moving = False
		return	

	# Write to pins
	def set_pin(self,data,bank):
		try:
			if bank == self.BANK_A:
				bus.write_byte_data(self.address,0x12,data)
			else:
				bus.write_byte_data(self.address,0x13,data)
		except IOError, e:
			print e
		return

			# Turn the motor
	def turn(self,steps,direction):
		global CLOCKWISE
		self.stop()
		self.moving = True
		self.steps = steps		
		while self.steps > 0:
			if direction == self.CLOCKWISE:
				for pin in range(len(out1)):
					pins = 0 	
					if out1[pin] > 0:
						pins = pins|self.pin1
					if out2[pin] > 0:
						pins = pins|self.pin2
					if out3[pin] > 0:
						pins = pins|self.pin3
					if out4[pin] > 0:
						pins = pins|self.pin4
					self.set_pin(pins,self.bank)
					time.sleep(self.speed)
				self.incrementPosition()
			else:
				for pin in reversed(range(len(out1))):
					pins = 0 	
					if out1[pin] > 0:
						pins = pins|self.pin1
					if out2[pin] > 0:
						pins = pins|self.pin2
					if out3[pin] > 0:
						pins = pins|self.pin3
					if out4[pin] > 0:
						pins = pins|self.pin4
					self.set_pin(pins,self.bank)
					time.sleep(self.speed)
				self.decrementPosition()
			self.steps -= 1
			if self.halt:
				break
		self.stop()
		return

	def interrupt(self):
		self.halt = True
		return

	# Increment current position 
	def incrementPosition(self):
		self.position += 1
		if self.position >= self.REVOLUTION:
			self.position -= self.REVOLUTION
		return self.position

	# Increment current position 
	def decrementPosition(self):
		self.position -= 1
		if self.position < 0:
			self.position += self.REVOLUTION
		return self.position

	# Increment current position 
	def zeroPosition(self):
		self.position = 0
		return self.position

	# Is the motor running (Future use)
	def isRunning(self):
		return self.running

	# Goto a specific position
	def goto(self, position):
		newpos = position

		while newpos > self.REVOLUTION:
			newpos -= self.REVOLUTION
		
		delta =  newpos - self.position

		# Figure which direction to turn
		if delta > self.REVOLUTION/2:
			delta = self.REVOLUTION/2 - delta

		elif delta < (0-self.REVOLUTION/2):
			delta = self.REVOLUTION + delta

		# Turn the most the efficient direction
		if delta > 0:
			self.turn(delta,self.CLOCKWISE)

		elif delta < 0:
			delta = 0 - delta
			self.turn(delta,self.ANTICLOCKWISE)

		self.position = newpos
		if self.position == self.REVOLUTION:
			self.position = 0
		return self.position			

	# Stop the motor (calls reset)
	def stop(self):
		self.reset()	
		return

	# Lock the motor (also keeps motor warm)
	def lock(self):
		self.set_pin(self.pin1|self.pin4,self.bank)
		self.moving = False
		return	

	# Set speed of motor
	def setSpeed(self,speed):
		self.speed = speed
		return

	        # Set Full Step Drive
        def setFullStepDrive(self):
                global out1,out2,out3,out4
                global Aout1,Aout2,Aout3,Aout4
                out1 = Aout1
                out2 = Aout2
                out3 = Aout3
                out4 = Aout4
                self.speed = self.NORMAL
                return

        # Set Half Step Drive
        def setHalfStepDrive(self):
                global out1,out2,out3,out4
                global Bout1,Bout2,Bout3,Bout4
                out1 = Bout1
                out2 = Bout2
                out3 = Bout3
                out4 = Bout4
                self.speed = self.NORMAL
                return

        # Set Wave Drive
        def setWaveDrive(self):
                global out1,out2,out3,out4
                global Cout1,Cout2,Cout3,Cout4
                out1 = Cout1
                out2 = Cout2
                out3 = Cout3
                out4 = Cout4
                self.speed = self.NORMAL * 2/3
                return

	
	# Get motor position
	def getPosition(self):
		return self.position
		

# End of Motor class
