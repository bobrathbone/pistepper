#!/bin/bash
# $Id: create_tar.sh,v 1.8 2025/08/01 06:35:31 bob Exp $

FILELIST=" test_unipolar_class.py unipolar_class.py single_motor.py test_position.py motord.py motor_daemon.py log_class.py bipolar_class.py test_nema17.py test_26_nema17.py test_motor_i2c_class.py motor_i2c_class.py README RPi" 

# Create robot software tar file
tar --exclude=CVS -cvzf  pi_stepper_motor.tar.gz ${FILELIST}

