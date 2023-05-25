#!/usr/bin/env python3
#
# Raspberry Pi Dual Stepper Motor motor daemon for background running
# Author : Bob Rathbone
# $Id: motord.py,v 1.10 2023/05/23 10:42:40 bob Exp $
# Site   : http://www.bobrathbone.com
#
# Hardware 28BYJ-48 Stepper motor (Bipolar) - Dual motor A and B test
# Motor driven  by a ULN2803A Eight Darlington outputs Driver Chip
# Uses the unipolar_class.py low level driver

import os
import sys
import pwd
import time
import signal

# Class imports
from unipolar_class import Motor
from motor_daemon import Daemon
from log_class import Log

# Define logging
log = Log()

# Motor definitions
motora = Motor(17,18,27,22)
motorb = Motor(4,25,24,23)
running = True

VERSION = '1.0'

class MyDaemon(Daemon):

    def finish():
        log.message('Finish' , log.INFO)
        global motora
        global motorb
        motora.stop()
        motorb.stop()
        return

    def sig_hup(self,signal,frame):
        global running
        global motora
        global motorb
        motora.interrupt()
        motorb.interrupt()
        running = False
        log.message('SIGHUP  recieved' , log.INFO)
        return


    def run(self):
        global running
        log.init('motor')
        msg = 'Motor daemon running pid ' + str(os.getpid())
        print(msg)
        log.message(msg, log.INFO)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGHUP, self.sig_hup)

        motora.init()
        motorb.init()
        motora.lock()
        motorb.lock()

        # Main run loop 
        while running:

            try: 
                # Fork a process to handle Motor A
                aPid = os.fork()    
                log.message('Stepper motor A running pid ' + str(aPid), log.INFO)
                if aPid == 0:
                    motora.turn(1*Motor.REVOLUTION, Motor.CLOCKWISE)
                    motora.lock()
                    time.sleep(2)
                    motora.turn(1*Motor.REVOLUTION, Motor.ANTICLOCKWISE)
                    os._exit(0)
                
                # Fork a process to handle Motor B
                bPid = os.fork()    
                log.message('Stepper motor B running pid ' + str(aPid), log.INFO)
                if bPid == 0:
                    motorb.turn(1*Motor.REVOLUTION, Motor.ANTICLOCKWISE)
                    motorb.lock()
                    time.sleep(2)
                    motorb.turn(1*Motor.REVOLUTION, Motor.CLOCKWISE)
                    os._exit(0)

                log.message('Motor A pid ' + str(aPid), log.INFO)
                log.message('Motor B pid ' + str(bPid), log.INFO)

                # Wait until both motors have stopped
                pid,status = os.waitpid(aPid, 0)
                log.message('Finished A status ' + str(status), log.INFO)
                pid,status = os.waitpid(bPid, 0)
                log.message('Finished B status ' + str(status), log.INFO)
                motora.lock()
                motorb.lock()
                time.sleep(5)

                # Stop the motors
                motora.stop()
                motorb.stop()
                msg = 'Motor daemon exiting'
                print(msg)
                log.message(msg, log.INFO)
                sys.exit()

            except KeyboardInterrupt:
                print("Keyboard interrupt - exiting")
                sys.exit()

    def status(self):
        # Get the pid from the pidfile
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "Motor daemon status: not running"
            log.message(message, log.INFO)
            print (message)
        else:
            message = "Motor daemon running pid " + str(pid)
            log.message(message, log.INFO)
            print (message )
        return

# End of class overrides

def usage():
    print ("usage: sudo %s start|stop|restart|status|nodaemon|version" % sys.argv[0])

### Main routine ###
if __name__ == "__main__":

    if pwd.getpwuid(os.geteuid()).pw_uid > 0:
        print("This program must be run with sudo or root permissions!")
        usage()
        sys.exit(1)

    daemon = MyDaemon('/var/run/motord.pid')
    log.init('motor')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'nodaemon' == sys.argv[1]:
            daemon.nodaemon()
        elif 'status' == sys.argv[1]:
            daemon.status()
        elif 'version' == sys.argv[1]:
            print ("Version " + VERSION)
        else:
            print ("Unknown command: " + sys.argv[1])
            sys.exit(2)
        sys.exit(0)
    else:
        usage()
        sys.exit(2)

# End of program

