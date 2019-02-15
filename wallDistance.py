from EncoderServo import initEncoders
from EncoderServo import calibrateSpeeds
from EncoderServo import setSpeedsIPS
from EncoderServo import getSpeeds
from EncoderServo import initEncoders
from EncoderServo import getMaxLeftFwd
from EncoderServo import getMaxRightFwd
import sys
import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO
import signal
import math
import random


#initEncoders and calibrate our servos
initEncoders()
calibrateSpeeds()
# Connect the left sensor and start measurement
GPIO.output(LSHDN, GPIO.HIGH)
time.sleep(0.01)
lSensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

# Connect the right sensor and start measurement
GPIO.output(RSHDN, GPIO.HIGH)
time.sleep(0.01)
rSensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

# Connect the front sensor and start measurement
GPIO.output(FSHDN, GPIO.HIGH)
time.sleep(0.01)
fSensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

#Set our speed going forward in a straight line 
setSpeedIPS(.55,.55)
while True:
    # Get a measurement from each sensor
    lDistance = lSensor.get_distance()
    fDistance = fSensor.get_distance()
    rDistance = rSensor.get_distance()
    
	if fDistance <= 5:
		break
    # Print each measurement
    print("Left: {}\tFront: {}\tRight: {}".format(lDistance, fDistance, rDistance))
setSpeedIPS(0,0)
# Stop measurement for all sensors
lSensor.stop_ranging()
fSensor.stop_ranging()
rSensor.stop_ranging()


