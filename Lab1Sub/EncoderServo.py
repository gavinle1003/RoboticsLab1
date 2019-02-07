# This program demonstrates usage of the servos.
# Keep the robot in a safe location before running this program,
# as it will immediately begin moving.
# See https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/ for more details.

import sys
import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO
import signal
import math
import random

rCount = 0   #current count for each wheel
lCount = 0   
prc = 0      #previous count
plc = 0

# For calibrate speeds, contains acccurate speeds
leftFwdSpeeds = {}
rightFwdSpeeds = {}
leftBwdSpeeds = {}
rightBwdSpeeds = {}

startTime = time.time()    #current timer

# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.
def ctrlC(signum, frame):
    print("Exiting")
    # Stop the servos
    pwm.set_pwm(LSERVO, 0, 0);
    pwm.set_pwm(RSERVO, 0, 0);
    #GPIO.cleanup()
    exit()

# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)
    
# Set the pin numbering scheme to the numbering shown on the robot itself.
GPIO.setmode(GPIO.BCM)
	


################ Encoder Functions #################

# Pins that the encoders are connected to
LENCODER = 17
RENCODER = 18

# This function is called when the left encoder detects a rising edge signal.
def onLeftEncode(pin):
    global lCount
    lCount = lCount + 1

# This function is called when the right encoder detects a rising edge signal.
def onRightEncode(pin):
    global rCount
    rCount = rCount + 1

# Resets tick counts to zero, store ticks before resetting
def resetCounts():
    global rCount
    global prc
    global lCount
    global plc
    global startTime
    prc = rCount
    plc = lCount
    rCount = 0
    lCount = 0
    
    #Reset time
    startTime = time.time()

# Returns the left and right tick counts since the last reset/start
# returns a tuple of left and right wheel speeds
def getCounts():
    global prc
    global plc
    return (plc, prc)

# Returns the instantaneous left and right wheel speeds as a tuple
# as revolutions per second;
def getSpeeds():
    global startTime
    currTime = time.time()
    global lcount
    global rcount
    if (lCount > 0):
        lSpeed =  (lCount / 32) / (currTime - startTime)
    else:
        lSpeed = 0
    if (rCount > 0):
        rSpeed =  (rCount / 32) / (currTime - startTime) 
    else:
        rSpeed = 0
    return (lSpeed, rSpeed)



	

# Code necessary to initialize the encoders
def initEncoders():
# Set encoder pins as input
# Also enable pull-up resistors on the encoder pins
# This ensures a clean 0V and 3.3V is always outputted from the encoders.
    GPIO.setup(LENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Attach a rising edge interrupt to the encoder pins
    GPIO.add_event_detect(LENCODER, GPIO.RISING, onLeftEncode)
    GPIO.add_event_detect(RENCODER, GPIO.RISING, onRightEncode)
    
    onLeftEncode(LENCODER)
    onRightEncode(RENCODER)
    
#Start the timer
    startTime = time.time()
    

################ Servo Functions ###################

# Write an initial value of 1.5, which keeps the servos stopped.
# Due to how servos work, and the design of the Adafruit library, 
# the value must be divided by 20 and multiplied by 4096.

# The servo hat uses its own numbering scheme within the Adafruit library.
# 0 represents the first servo, 1 for the second, and so on.
LSERVO = 0
RSERVO = 1
    
# Initialize the servo hat library.
pwm = Adafruit_PCA9685.PCA9685()

# 50Hz is used for the frequency of the servos.
pwm.set_pwm_freq(50)

pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096))
pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096))


#Dictionary to initialize we will use our set speed as the key and it speed measurement as the value
#for our key value pair this will help us translate our user input into a new speed
#for RPS and IPS
def calibrateSpeeds():
    global SpeedData
    global startTime

    #Calibrate Left wheel
    i = 140
    while i < 150:
        x = float(i/100)
        resetCounts()
        startTime = time.time()
        pwm.set_pwm(LSERVO, 0, math.floor(x / 20 * 4096))
        pwm.set_pwm(RSERVO, 0, math.floor(x / 20 * 4096))
        time.sleep(2)
#gets speeds of wheels after it changes we will need to add in time wait for the specified number of seconds.
#along with a 1 second interval
        y = getSpeeds()

#each time we get these speeds we will enter the values into our dictionary
#this will make it easier to print our graph
        leftBwdSpeeds[x] = y[0]
        rightFwdSpeeds[x] = y[1]
        
        i+=5
        
        
    
#Add the value for stopped to all four maps
    x = float(i/100)
    resetCounts()
    startTime = time.time()
    pwm.set_pwm(LSERVO, 0, math.floor(x / 20 * 4096))
    pwm.set_pwm(RSERVO, 0, math.floor(x / 20 * 4096))
    time.sleep(2)
#gets speeds of wheels after it changes we will need to add in time wait for the specified number of seconds.
#along with a 1 second interval
    y = getSpeeds()

#each time we get these speeds we will enter the values into our dictionary
#this will make it easier to print our graph
    leftFwdSpeeds[x] = y[0]
    leftBwdSpeeds[x] = y[0]
    rightFwdSpeeds[x] = y[1]
    rightBwdSpeeds[x] = y[1]
    
        
    i+=5
        
    
    
    

    
#Calibrate Right Wheel
    while i <=160:
        x = float(i/100)
        resetCounts()
        startTime = time.time()
        pwm.set_pwm(LSERVO, 0, math.floor(x / 20 * 4096))
        pwm.set_pwm(RSERVO, 0, math.floor(x / 20 * 4096))
        time.sleep(2)

        y = getSpeeds()

        rightBwdSpeeds[x] = y[1]
        leftFwdSpeeds[x] = y[0]
        
        i+=5
        
       

    pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096))
    pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096))


 
#Set the speed of the motors based on RPS
#Negative RPS goes backwards
def setSpeedsRPS(rpsLeft, rpsRight):
    LPWM = 1.5
    RPWM = 1.5
    LfloorPWM = 1.5
    LceilingPWM = 1.5
    RfloorPWM = 1.5
    RceilingPWM = 1.5
    
    
#Forwards Left 
    if(rpsLeft > 0):
#rpsLeft is faster than what is possible
        if(leftFwdSpeeds[1.6] <= rpsLeft):
            LPWM = 1.6
        else:
#rpsLeft is in between 1.4 and 1.45 pwm
            if((leftFwdSpeeds[1.6] >= rpsLeft) and (rpsLeft > leftFwdSpeeds[1.55])):
                LfloorPWM = 1.55
                LceilingPWM = 1.6
#rpsLeft is in between 1.45 and 1.5 pwm
            if((leftFwdSpeeds[1.55] >= rpsLeft) and (rpsLeft > leftFwdSpeeds[1.5])):
                LfloorPWM = 1.5
                LceilingPWM = 1.55
        
#Find slope based on floor and ceiling, where PWM is y and rps is x
            slope = float((LceilingPWM - LfloorPWM) / (leftFwdSpeeds[LceilingPWM] - leftFwdSpeeds[LfloorPWM]))
            LPWM = float((slope * rpsLeft) + 1.5)  #1.5 is stopped, so our y-intercept
        
#Backwards Left        
    if(rpsLeft < 0):
#rpsLeft is faster than what is possible
        if(leftBwdSpeeds[1.4] <= (rpsLeft * -1)):
            LPWM = 1.4
        else:
#rpsLeft is in between 1.4 and 1.45 pwm
            if((leftBwdSpeeds[1.4] >= (rpsLeft * -1)) and ((rpsLeft * -1) > leftBwdSpeeds[1.45])):
                LfloorPWM = 1.45
                LceilingPWM = 1.4
#rpsLeft is in between 1.45 and 1.5 pwm
            if((leftBwdSpeeds[1.45] >= (rpsLeft * -1)) and ((rpsLeft * -1) > leftBwdSpeeds[1.5])):
                LfloorPWM = 1.5
                LceilingPWM = 1.45
        
#Find slope based on floor and ceiling, where PWM is y and rps is x
            slope = float((LceilingPWM - LfloorPWM) / (leftBwdSpeeds[LceilingPWM] - leftBwdSpeeds[LfloorPWM]))
            LPWM = float((slope * (rpsLeft * -1)) + 1.5)  #1.5 is stopped, so our y-intercept
              
#Forwards Right
    if(rpsRight > 0):
#rpsLeft is faster than what is possible
        if(rightFwdSpeeds[1.4] <= rpsRight):
            RPWM = 1.4
        else: 
#rpsLeft is in between 1.4 and 1.45 pwm
            if((rightFwdSpeeds[1.4] >= rpsRight) and (rpsRight > rightFwdSpeeds[1.45])):
                RfloorPWM = 1.45
                RceilingPWM = 1.4
#rpsLeft is in between 1.45 and 1.5 pwm
            if((rightFwdSpeeds[1.45] >= rpsRight) and (rpsRight > rightFwdSpeeds[1.5])):
                RfloorPWM = 1.5
                RceilingPWM = 1.45
            
#Find slope based on floor and ceiling, where PWM is y and rps is x
            slope = float((RceilingPWM - RfloorPWM) / (rightFwdSpeeds[RceilingPWM] - rightFwdSpeeds[RfloorPWM]))
            RPWM = float((slope * rpsRight) + 1.5)  #1.5 is stopped, so our y-intercept
        
#Backwards Right
    if(rpsRight < 0):
#rpsLeft is faster than what is possible
        if(rightBwdSpeeds[1.6] <= (rpsRight * -1)):
            RPWM = 1.6
        else: 
#rpsLeft is in between 1.4 and 1.45 pwm
            if((rightBwdSpeeds[1.6] >= (rpsRight * -1)) and ((rpsRight * -1) > rightBwdSpeeds[1.55])):
                RfloorPWM = 1.55
                RceilingPWM = 1.6
#rpsLeft is in between 1.45 and 1.5 pwm
            if((rightBwdSpeeds[1.55] >= (rpsRight * -1)) and ((rpsRight * -1) > rightBwdSpeeds[1.5])):
                RfloorPWM = 1.5
                RceilingPWM = 1.55
            
#Find slope based on floor and ceiling, where PWM is y and rps is x
            slope = float((RceilingPWM - RfloorPWM) / (rightBwdSpeeds[RceilingPWM] - rightBwdSpeeds[RfloorPWM]))
            RPWM = float((slope * (rpsRight * -1)) + 1.5)  #1.5 is stopped, so our y-intercept
        

#Set the speeds based off of the calculations
    pwm.set_pwm(LSERVO, 0, math.floor(LPWM / 20 * 4096))
    pwm.set_pwm(RSERVO, 0, math.floor(RPWM / 20 * 4096))
    
    
#Set the speed based on inches per second
def setSpeedsIPS(ipsLeft, ipsRight):

#We know how many inches is a full rotation and we can go ahead and see how many rotations we want to travel and then apply it
	circumference = 3.14 * 2.61
#inches per sec can be turned to RPS by dividing what was traveled by the total circumference of the wheel
	ILeft = ipsLeft/circumference
	IRight = ipsRight/circumference
#Then we plug in here in order to set the speeds using our RPS function and the speeds used in its dictionaries
	setSpeedsRPS(ILeft,IRight)

    
#Set the speed of the robot so that the robot will move with a linear speed given by
#the parameter 'v' (in inches per second) with an angular velocity 'w' (radians per second)
#Positive angular velocities should make the robot spin counterclockwise
def setSpeedsvw(v, w):
    absAngular = abs(w)
#We will get our Radius again by using our velocity and angular velocity
    Radius = abs(v/w)

#Dmid is about 2 inches
    dMid = 2
#We get our velocities for left and right wheel
    vRight = absAngular * (Radius + dMid)
    vLeft = absAngular * (Radius - dMid)
    
    if w < 0:
        setSpeedsIPS(vRight, vLeft)
    else:
        setSpeedsIPS(vLeft, vRight)
        
    
def getMaxLeftFwd():
    #1.6
    return leftFwdSpeeds[1.6]   

def getMaxRightFwd():
    #1.3
    return rightFwdSpeeds[1.4]
    
def getMaxLeftBwd():
    #1.3
    return leftBwdSpeeds[1.4]

def getMaxRightBwd():
    #1.6
    return rightBwdSpeeds[1.6]
	