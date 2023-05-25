#!/bin/bash
# $Id: create_tar.sh,v 1.7 2023/05/25 06:52:39 bob Exp $

FILELIST=" test_unipolar_class.py unipolar_class.py single_motor.py test_position.py motord.py motor_daemon.py log_class.py bipolar_class.py test_nema17.py test_26_nema17.py test_motor_i2c_class.py motor_i2c_class.py README" 

# Create robot software tar file
tar -cvzf  pi_stepper_motor.tar.gz ${FILELIST}

