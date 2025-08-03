Raspberry Pi Stepper Motor Project pistepper
============================================
Version 2.3 - 3rd August 2025
Use LGPIO library to drive the **Nema17** stepper motor. New class **bipolar_lgpio_class.py** added.

This project has been designed to help students or hobbyists get started with driving stepper motors on the Raspberry PI. It covers two types of stepper motor namely unipolar and bipolar.

It includes code to either drive either
  • One or two x 5-Wire "28BYJ-48" stepper Motor (bipolar motor) with ULN2803A driver
Or
  • A 12-volt #324 (Nema17) high torque stepper motor (unipolar motor) with H-Driver circuit (using either RPi.GPIO or LGPIO libraries)


More details can be found at :

https://bobrathbone.com/raspberrypi/stepper_motor.html


The software is maintained in the following GitHub repository.
https://github.com/bobrathbone/pistepper

To download the software, go to your home directory and download the software using the **git clone** command shown below:
```
$ cd
$ git clone https://github.com/bobrathbone/pistepper
```

This will download the development files into the pistepper directory. Change to **pistepper** directory.
```
$ cd pistepper
```

