#!/usr/bin/env python3
#
# $Id: bipolar_class.py,v 1.11 2025/09/18 08:58:42 bob Exp $
# Raspberry Pi bipolar Stepper Motor Driver Class
# Hardware Nema17 12 Volt Stepper High Torque Motor
# Gear Reduction Ratio: 1/64 
# Uses the A4988 H-bridge circuit driver board.
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#

import sys
import os
import time

import RPi.GPIO as GPIO

# The stepper motor can be driven in five different modes 
# See http://en.wikipedia.org/wiki/Stepper_motor

# Step resolution (The last column is the multiplier for one revolution)
FullStep = [0,0,0,1]
HalfStep = [1,0,0,2]
QuarterStep = [0,1,0,4]
EighthStep = [1,1,0,8]
SixteenthStep = [1,1,1,16]

# Other definitions
ENABLE = GPIO.LOW
DISABLE = GPIO.HIGH
STEPS = 200 # 200 step motor (Full)

class Motor:
    # Direction
    CLOCKWISE = 0
    ANTICLOCKWISE = 1

    # Step sizes (Don't change values)
    FULL = 1
    HALF = 2
    QUARTER = 4
    EIGHTH = 8
    SIXTEENTH = 16

    pulse=0.0007
    interval=0.0007
    oneRevolution = STEPS
    _reverse = False  # Reverse motor polarity (if cable crossed over)

    def __init__(self, step, direction, enable, ms1, ms2, ms3):
        self.step = step
        self.direction = direction
        self.enable = enable
        self.ms1 = ms1
        self.ms2 = ms2
        self.ms3 = ms3
        return

    # Initialise GPIO pins for this unipolar motor
    def init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.direction,GPIO.OUT)
        GPIO.setup(self.step,GPIO.OUT)
        GPIO.setup(self.enable,GPIO.OUT)
        GPIO.setup(self.ms1,GPIO.OUT)
        GPIO.setup(self.ms2,GPIO.OUT)
        GPIO.setup(self.ms3,GPIO.OUT)
        self.zeroPosition()
        self.setStepSize(self.FULL)
        return  

    # Reverse motor polarity
    def reverse(self,_reverse=False):
        self._reverse = _reverse

    def isReversed(self):
        return self._reverse

    # Reset (stop) motor
    def reset(self):
        GPIO.output(self.step,GPIO.LOW)
        GPIO.output(self.direction,GPIO.LOW)
        GPIO.output(self.enable,GPIO.HIGH)
        GPIO.output(self.ms1,GPIO.LOW)
        GPIO.output(self.ms2,GPIO.LOW)
        GPIO.output(self.ms3,GPIO.LOW)
        return  

    # Set up stepper resolution
    def setStepResolution(self,stepres):
        GPIO.output(self.ms1,stepres[0])
        GPIO.output(self.ms2,stepres[1])
        GPIO.output(self.ms3,stepres[2])
        self.oneRevolution = STEPS * stepres[3]
        return self.oneRevolution

    # Turn the motor
    def turn(self,steps,motor_dir):

        if self._reverse:   # Reverse motor polarity
            if motor_dir == self.CLOCKWISE:
                motor_dir = self.ANTICLOCKWISE
            elif motor_dir == self.ANTICLOCKWISE:
                motor_dir = self.CLOCKWISE
        GPIO.output(self.direction,motor_dir)

        count = steps
        GPIO.output(self.enable,ENABLE)
        while count > 0:
            GPIO.output(self.step,GPIO.HIGH)
            time.sleep(self.pulse)
            GPIO.output(self.step,GPIO.LOW)
            time.sleep(self.interval)
            count -= 1
        GPIO.output(self.enable,DISABLE)
        return

    def interrupt(self):
        self.halt = True
        return

    # set current position as 1 
    def zeroPosition(self):
        self.position = 1
        return self.position

    # Set starting position (1)
    def startPosition(self):
        self.position = 1
        return self.position

    def getPosition(self):
        return self.position

    # Goto a specific position
    def goto(self, position):
        newpos = position
        while newpos > self.oneRevolution:
                newpos -= self.oneRevolution

        delta =  newpos - self.position

        # Figure which direction to turn
        if delta > self.oneRevolution/2:
            delta = self.oneRevolution/2 - delta

        elif delta < (0-self.oneRevolution/2):
                delta = self.oneRevolution + delta

        # Turn the most the efficient direction
        if delta > 0:
                self.turn(delta,self.CLOCKWISE)

        elif delta < 0:
                delta = 0 - delta
                self.turn(delta,self.ANTICLOCKWISE)

        self.position = newpos
        if self.position == self.oneRevolution:
                self.position = 0
        return self.position


    # Stop the motor (calls reset)
    def stop(self):
        self.reset()    

    # Lock the motor (also keeps motor warm)
    def lock(self):
        GPIO.output(self.enable,ENABLE)

    # Lock the motor (also keeps motor warm)
    def unlock(self):
        GPIO.output(self.enable,DISABLE)

    # Set Step size
    def setStepSize(self,size):

        if size == self.HALF:
            steps = self.setStepResolution(HalfStep)    
        elif size == self.QUARTER:
            steps = self.setStepResolution(QuarterStep) 
        elif size == self.EIGHTH:
            steps = self.setStepResolution(EighthStep)  
        elif size == self.SIXTEENTH:
            steps = self.setStepResolution(SixteenthStep)   
        else:
            steps = self.setStepResolution(FullStep)    

        self.oneRevolution = steps
        return self.oneRevolution

    # Get number of revolution steps
    def getRevolution(self):
        return self.oneRevolution
        
    # Lock the motor in the current position
    def lock(self):
        GPIO.setup(self.enable,GPIO.OUT)

    # Unlock the motor (motor will get hot after a while)
    def unlock(self):
        GPIO.setup(self.enable,GPIO.OUT)

# End of Unipolar Motor class

# Test routine
if __name__ == '__main__':

    # GPIO assignments for 26-pin header for older Raspberry Pi's
    '''
    step = 24
    direction = 4
    enable = 25
    ms1 = 23
    ms2 = 22
    ms3 = 27
    '''

    # 40 pin header for newer Raspberry Pi's
    step = 21
    direction = 20
    enable = 25
    ms1 = 18
    ms2 = 15
    ms3 = 14

    motora = Motor(step,direction,enable,ms1,ms2,ms3)
    print("Test Neva17 bipolar motor")
    print("GPIO settings")
    print("  step",step)
    print("  direction",direction)
    print("  enable",enable)
    print("  ms1",ms1)
    print("  ms2",ms2)
    print("  ms3",ms3)

    time.sleep(2)

    # Initialise motor (Sets current position to 1)
    motora.init()
    #motora.reverse(True)   # Uncomment to reverse motor polarity

    # Set the motor to step size FULL (1)
    print ("Motor A Clockwise FULL step")
    revolution = motora.setStepSize(Motor.FULL)
    motora.turn(revolution, Motor.CLOCKWISE)
    time.sleep(2)

    print ("Motor A Anti-clockwise FULL step")
    motora.turn(revolution, Motor.ANTICLOCKWISE)
    time.sleep(2)

    # Close the motor
    motora.reset()
    motora.unlock()
    print ("Motor A end of test")

# End of test program

# set tabstop=4 shiftwidth=4 expandtab
# retab

