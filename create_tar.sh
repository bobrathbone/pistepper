#!/bin/bash
# $Id: create_tar.sh,v 1.1 2013/12/23 11:26:41 bob Exp $

FILELIST="log_class.py motor_daemon.py motor_i2c_class.py motor_class.py motord.py test_motor_class.py test_motor_i2c_class.py"

# Create robot software tar file
tar -cvzf  pi_stepper_motor.tar.gz ${FILELIST}

