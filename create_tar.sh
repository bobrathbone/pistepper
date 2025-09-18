#!/bin/bash
# $Id: create_tar.sh,v 1.15 2025/08/26 10:54:08 bob Exp $

TARFILE=pi_stepper_motor.tar.gz

FILELIST=" luma_class.py test_unipolar_class.py unipolar_class.py single_motor.py test_position.py motord.py motor_daemon.py log_class.py bipolar_class.py bipolar_lgpio_class.py test_nema17.py test_26_nema17.py test_motor_i2c_class.py motor_i2c_class.py button_class_gpiozero.py rotary_class_gpiozero.py control_nema17.py test_gpios.py README README.md RPi" 

# Create robot software tar file
tar --exclude=CVS --exclude=__pycache__ -cvzf ${TARFILE} ${FILELIST}
echo "Created ${TARFILE}"
