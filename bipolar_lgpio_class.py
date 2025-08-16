#!/usr/bin/env python3
#
# $Id: bipolar_lgpio_class.py,v 1.15 2025/08/16 09:02:23 bob Exp $
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
ENABLE = LOW
DISABLE = HIGH
STEPS = 200 # 200 step motor (Full)

class Motor:
    # Direction
    CLOCKWISE = 0
    ANTICLOCKWISE = 1

    # Step sizes (Don't change values)
    FULL = 1        # 200 steps
    HALF = 2        # 400 steps
    QUARTER = 4     # 800 steps
    EIGHTH = 8      # 1600 steps
    SIXTEENTH = 16  # 3200 steps

    pulse=0.0007
    interval=0.0007
    oneRevolution = STEPS # If FULL step size
    position = 1    # Current position (200 x stepsize)
    debug = False   # Print debug statements
    halt = False    # Interrupt turn routine

    sDirection = ("CLOCKWISE","ANTICLOCKWISE")

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
        lgpio.gpio_write(self.chip,self.enable,DISABLE)
        self.setStepSize(self.FULL)
        self.startPosition()
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

    # Lock the motor (also keeps motor warm)
    def lock(self):
        self.halt = True    # Stop motor
        lgpio.gpio_write(self.chip,self.enable,ENABLE)

    # Unlock the motor (motor will get hot after a while) 
    def unlock(self):
        lgpio.gpio_write(self.chip,self.enable,DISABLE)

    # Reset (stop) motor
    def reset(self):
        lgpio.gpio_write(self.chip,self.step,LOW)
        lgpio.gpio_write(self.chip,self.direction,LOW)
        lgpio.gpio_write(self.chip,self.enable,DISABLE)
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
        if self.debug:
            print("Turn steps=%d %s revolution=%d position=%d" % 
                  (steps,self.sDirection[direction],self.oneRevolution,self.position))
        count = steps
        lgpio.gpio_write(self.chip,self.direction,direction)
        lgpio.gpio_write(self.chip,self.enable,ENABLE)
        while count > 0:
            lgpio.gpio_write(self.chip,self.step,HIGH)
            time.sleep(self.pulse)
            lgpio.gpio_write(self.chip,self.step,LOW)
            time.sleep(self.interval)
            count -= 1
            if self.halt:      # Check interrupt
                steps = count
                break
    
        # Calculate new position
        self.halt = False
        if direction == self.CLOCKWISE:
            self.position = self.position + steps 
            while self.position > self.oneRevolution:
                self.position -= self.oneRevolution 
        else:  # ANTICLOCKWISE
            self.position = self.position - steps 
            while self.position < 1:
                self.position += self.oneRevolution 
        if self.debug:
            print("New position=%d" % self.position)
        return self.position

    def interrupt(self):
        self.halt = True

    def close(self):
        lgpio.gpiochip_close(self.chip)

    # Set starting position (1)
    def startPosition(self):
        self.position = 1
        return self.position

    def getPosition(self):
        return self.position

    # Goto a specific position
    def goto(self,position=0,stepsize=FULL):
        self.setStepSize(stepsize)
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
        self.halt = True
        self.lock()    

    # Start the motor 
    def start(self):
        self.halt = False
        self.unlock()    

    # Set the position counter
    def setPosition(self,pos=1):
        self.position = pos 

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
        
    def setDebug(self,level):
        self.debug = level

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

    # Set debug to True or False
    motora.setDebug(False)

    # Set the motor to step size FULL (1) 
    print ("Motor A Clockwise FULL step")
    revolution = motora.setStepSize(Motor.FULL)
    motora.turn(revolution, Motor.CLOCKWISE)
    time.sleep(2)
   
    print ("Motor A Anti-clockwise FULL step")
    motora.turn(revolution, Motor.ANTICLOCKWISE)
    time.sleep(2)

    print ("Motor A Clockwise 3 revolutions FULL step")
    motora.turn(revolution*3, Motor.CLOCKWISE)
    time.sleep(1)

    print ("Motor A Anticlockwise FULL step")
    motora.turn(revolution, Motor.ANTICLOCKWISE)
    time.sleep(1)

    print ("Motor A Clockwise Sixteenth step")
    revolution = motora.setStepSize(Motor.SIXTEENTH)
    motora.turn(revolution/2, Motor.CLOCKWISE)
    time.sleep(1)

    # Turn to a specific position
    print ("Motor A goto specific positions")
    revolution = motora.setStepSize(Motor.FULL)
    for pos in (50, 100, 75, 50):
        print ("  Goto",pos,"revoution",revolution)
        motora.goto(pos)
        time.sleep(0.5)
    time.sleep(2)

    print ("Motor A go CLOCKWISE in 16 x 12 steps")
    revolution = motora.setStepSize(Motor.FULL)
    step = 12
    count = 1
    x = range(12, 200, step)
    for pos in x: 
        print("  %d Goto position %d" % (count,pos))
        motora.goto(pos)
        count += 1
        if count > 12:
            motora.stop()
            break
        time.sleep(0.5)
      
    print ("Motor A Go to position 100")
    motora.goto(100,motora.FULL)
    time.sleep(2)
    print ("Motor A Go to position 1")
    motora.goto(1,motora.FULL)

    print("Unlock motora")
    motora.unlock()
    time.sleep(4)
    print("Lock motora")
    motora.lock()
    time.sleep(6)

    # Close the motor
    motora.reset()
    motora.close()
    print ("Motor A end of test")
# End of test program

# set tabstop=4 shiftwidth=4 expandtab
# retab
