#!/usr/bin/env python3
# Raspberry Pi test all available GPIOs
#
# $Id: test_gpios.py,v 1.2 2023/05/22 13:54:39 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#            The authors shall not be liable for any loss or damage however caused.
#

import RPi.GPIO as GPIO
import sys,time 
import pdb

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pins = (17,18,27,22)    # Motor A 
#pins = (4,25,24,23)    # Motor B 
delay = 0.6

# Main program
for idx in range (0,len(pins)):
    try:
        pin = pins[idx]
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,GPIO.LOW)

    except Exception as e:
        print("Error: GPIO",gpio_pin, e)     
        sys.exit(1)

while True: 
    try:
        for idx in range (0,len(pins)):
            pin = pins[idx]
            print("Pin GPIO",pin)
            GPIO.output(pin,GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(pin,GPIO.LOW)
            time.sleep(delay)

    except KeyboardInterrupt:
        print("\nEnd of GPIOs test")
        GPIO.cleanup()
        sys.exit(0)

# set tabstop=4 shiftwidth=4 expandtab
# retab
