#!/usr/bin/env python3
#
# $Id: log_class.py,v 1.4 2023/05/22 13:54:39 bob Exp $
# Raspberry Pi Stepper Motor
# Logging class
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com

import os
import logging

class Log:

    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    DEBUG = logging.DEBUG

    MotorLibDir = "/var/lib/motor"
    LogLevelFile = MotorLibDir + "/loglevel"

    module = ''
    level = logging.INFO

    def __init__(self):
        return 

    def init(self,module):
        self.module = module
        # Set up loglevel file
        if not os.path.isfile(self.LogLevelFile) or os.path.getsize(self.LogLevelFile) == 0:
            os.popen("mkdir -p " + self.MotorLibDir)
            os.popen("echo INFO > " + self.LogLevelFile)
        self.level = self.getLevel()
        return 

    def message(self,message,level):
        # Set up logging, level can be INFO, WARNING, ERROR, DEBUG
        logger = logging.getLogger('gipiod')
        hdlr = logging.FileHandler('/var/log/' + self.module + '.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(self.level)
        if level == logging.INFO:
            logger.info(message)
        if level == logging.WARNING:
            logger.warning(message)
        if level == logging.DEBUG:
            logger.debug(message)
        if level == logging.ERROR:
            logger.error(message)
        logger.removeHandler(hdlr)
        hdlr.close()
        return

    # Temporary set log level
    def setLevel(self,level):
        self.level = level
        return

    # Get the log level from the configuration file
    def getLevel(self):
        self.loglevel = logging.INFO
        if os.path.isfile(self.LogLevelFile):
            try:
                p = os.popen("cat " + self.LogLevelFile)
                strLogLevel = p.readline().rstrip('\n')
                if strLogLevel == "DEBUG":
                        self.loglevel = logging.DEBUG
                elif strLogLevel == "WARNING":
                        self.loglevel = logging.WARNING
                elif strLogLevel == "ERROR":
                        self.loglevel = logging.ERROR

            except ValueError:
                    self.loglevel = logging.INFO

        return self.loglevel

# End of log class

