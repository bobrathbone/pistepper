#!/usr/bin/env python3
#
# $Id: bipolar_lgpio_class.py,v 1.5 2025/08/03 11:57:32 bob Exp $
# Raspberry Pi bipolar Stepper Motor Driver Class
# Hardware Nema17 12 Volt Stepper High Torque Motor
# Gear Reduction Ratio: 1/64 
# Uses the A4988 H-bridge circuit driver board.
#
# This version was converted from bipolar_class.py to use the Pyton3 lgpio library
# See https://abyz.me.uk/lg/py_lgpio.html
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#

import sys
import os
import time

#import RPi.GPIO as GPIO
import lgpio

# The stepper motor can be driven in five different modes 
# See http://en.wikipedia.org/wiki/Stepper_motor

# Step resolution (The last column is the multiplier for one revolution)
# The first three parameters are the settings for ms1, ms2 and ms3 windings respectively 
FullStep = [0,0,0,1]
HalfStep = [1,0,0,2]
QuarterStep = [0,1,0,4]
EighthStep = [1,1,0,8]
SixteenthStep = [1,1,1,16]

# Other definitions
HIGH = 1
LOW = 0
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
        self.chip = self.get_chip()
        lgpio.gpio_claim_output(self.chip,self.direction,lgpio.SET_PULL_UP)
        lgpio.gpio_claim_output(self.chip,self.step,lgpio.SET_PULL_UP)
        lgpio.gpio_claim_output(self.chip,self.enable,lgpio.SET_PULL_UP)
        lgpio.gpio_claim_output(self.chip,self.ms1,lgpio.SET_PULL_UP)
        lgpio.gpio_claim_output(self.chip,self.ms2,lgpio.SET_PULL_UP)
        lgpio.gpio_claim_output(self.chip,self.ms3,lgpio.SET_PULL_UP)
        self.zeroPosition()
        self.setStepSize(self.FULL)
        return  

    # Open chip depending upon the Rasberry Pi model
    def get_chip(self): 
        # The Raspberry Pi Model 5 uses the RP1 chip (4). Try to open first
        if os.path.exists("/proc/device-tree/aliases/gpio4"):
            try:
                chip = lgpio.gpiochip_open(4)
                #print("Using RP1 chip",4,hex(chip))
            except Exception as e:
                print ("Fatal error: %s" % (str(e)))
                sys.exit(1)
        else:
            # Earlier Raspberry Pi 4b,3B etc uses SOC chip  for I/O (0).
            try:
                chip = lgpio.gpiochip_open(0)
                #print("Using chip",0,hex(chip))
            except Exception as e:
                print ("Fatal error: %s" % (str(e)))
                sys.exit(1)
        return chip

    # Reset (stop) motor
    def reset(self):
        lgpio.gpio_write(self.chip,self.step,LOW)
        lgpio.gpio_write(self.chip,self.direction,LOW)
        lgpio.gpio_write(self.chip,self.enable,LOW)
        lgpio.gpio_write(self.chip,self.ms1,LOW)
        lgpio.gpio_write(self.chip,self.ms2,LOW)
        lgpio.gpio_write(self.chip,self.ms3,LOW)
        return  

    # Set up stepper resolution
    def setStepResolution(self,stepres):
        lgpio.gpio_write(self.chip,self.ms1,stepres[0])
        lgpio.gpio_write(self.chip,self.ms2,stepres[1])
        lgpio.gpio_write(self.chip,self.ms3,stepres[2])
        self.oneRevolution = STEPS * stepres[3]
        return self.oneRevolution

    # Turn the motor
    def turn(self,steps,direction):
        count = steps
        lgpio.gpio_write(self.chip,self.enable,HIGH)
        lgpio.gpio_write(self.chip,self.direction,direction)
        while count > 0:
            lgpio.gpio_write(self.chip,self.step,HIGH)
            time.sleep(self.pulse)
            lgpio.gpio_write(self.chip,self.step,LOW)
            time.sleep(self.interval)
            count -= 1
        lgpio.gpio_write(self.chip,self.enable,LOW)
        return

    def interrupt(self):
        self.halt = True
        return

    def close(self):
        lgpio.gpiochip_close(self.chip)

    # Increment current position 
    def incrementPosition(self):
        return

    # Increment current position 
    def decrementPosition(self):
        return 

    # Increment current position 
    def zeroPosition(self):
        self.position = 0
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
        return

    # Lock the motor (also keeps motor warm)
    def lock(self):
        return  

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
        

# End of Unipolar Motor class

# Test routine
if __name__ == '__main__':
    # 40 pin header for newer Raspberry Pi's
    step = 21
    direction = 20
    enable = 25     # Not necessarily required (connect to control enable pin)
    ms1 = 18
    ms2 = 15
    ms3 = 14
    motora = Motor(step,direction,enable,ms1,ms2,ms3) 
    print("direction",direction)
    print("enable",enable)
    print("ms1",ms1)
    print("ms2",ms2)
    print("ms3",ms3)
    motora.init()

    # Get the number of steps per revoltion
    count = 3
    while count > 0:
        print ("Motor A Clockwise Full step")
        revolution = motora.setStepSize(Motor.FULL)
        motora.turn(revolution*3, Motor.CLOCKWISE)
        count -= 1
        time.sleep(1)

    count = 3
    while count > 0:
        print ("Motor A Anticlockwise Full step")
        revolution = motora.setStepSize(Motor.FULL)
        motora.turn(revolution*1, Motor.ANTICLOCKWISE)
        count -= 1
        time.sleep(1)

        print ("Motor A Clockwise Sixteenth step")
        revolution = motora.setStepSize(Motor.SIXTEENTH)
        motora.turn(revolution/2, Motor.CLOCKWISE)
        time.sleep(1)

    # Close the motor
    motora.reset()
    motora.close()
# End of test program

# set tabstop=4 shiftwidth=4 expandtab
# retab
