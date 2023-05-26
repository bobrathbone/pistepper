

Raspberry Pi Stepper Motor Project pistepper
============================================
Version 2.0 (Converted to Python)

This project has been designed to help students or hobbyists get started with driving stepper motors on the Raspberry PI. It covers two types of stepper motor namely unipolar and bipolar.

It includes code to either drive eitheR
  • One or two x 5-Wire "28BYJ-48" stepper Motor (bipolar motor) with ULN2803A driver
Or
  • A 12-volt #324 (Nema17) high torque stepper motor (unipolar motor) with H-Driver circuit


More details can be found at :

https://bobrathbone.com/raspberrypi/stepper_motor.html

Software can be dowloaded and installed  with the following:

Create a directory called /home/pi/stepper. Copy the pi_stepper_motor.tar.gz to the /home/pi/stepper directory or use wget to download it.

    wget http://www.bobrathbone.com/raspberrypi/packages/pi_stepper_motor.tar.gz

Un-tar the file with the following command:

    tar -xvf pi_stepper_motor.tar.gz

This will unzip the files to the /home/pi/stepper directory.


