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
#import plotly.plotly as py
#import plotly.graph_objs as go
import random

rCount = 0   #current count for each wheel
lCount = 0   
prc = 0      #previous count
plc = 0

# For calibrate speeds, contains acccurate speeds
leftFwdSpeeds = {'0.0':'1.5'}
rightFwdSpeeds = {'0.0':'1.5'}
leftBwdSpeeds = {'0.0':'1.5'}
rightBwdSpeeds = {'0.0':'1.5'}

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
    while i <=150:
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
        leftFwdSpeeds[y[0]] = x
        rightBwdSpeeds[y[1]] = x
        
        i+=5
        
        print("Left wheel forward speed: ", leftFwdSpeeds[y[0]], " RPS: ", y[0], "       Right wheel backward speed: ", rightBwdSpeeds[y[1]], " RPS: ", y[1])
    
    
    #Calibrate Right Wheel
    while i <=160:
        x = float(i/100)
        resetCounts()
        startTime = time.time()
        pwm.set_pwm(LSERVO, 0, math.floor(x / 20 * 4096))
        pwm.set_pwm(RSERVO, 0, math.floor(x / 20 * 4096))
        time.sleep(2)

        y = getSpeeds()

        rightFwdSpeeds[y[1]] = x
        leftBwdSpeeds[y[0]] = x
        
        i+=5
        
        print("Left wheel backwards speed: ", leftBwdSpeeds[y[0]], " RPS: ", y[0],"       Right wheel forward speed: ", rightFwdSpeeds[y[1]], " RPS: ", y[1])

    pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096))
    pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096))

 
#Set the speed of the motors based on RPS
#Negative RPS goes backwards
def setSpeedsRPS(rpsLeft, rpsRight):
    leftRpsFloor = -1
    leftRpsCeiling = -1
    leftPwmFloor = 0
    leftPwmCeiling = 0
    leftSpeed = 1.5
    
    rightRpsFloor = -1
    rightRpsCeiling = -1
    rightPwmFloor = 0
    rightPwmCeiling = 0
    rightSpeed = 1.5
    
    #Find the two calibrated RPS speeds closest to the inputted RPS
    
    if (rpsLeft >= 0):  #forwards left
        for rps, pwm in leftFwdSpeeds.items():
            #Find floor
            if(float(rps) < rpsLeft and (leftRpsFloor == -1 or (rpsLeft - float(rps) < leftRpsFloor - float(rps)))):
                leftRpsFloor = float(rps)
                leftPwmFloor = pwm
            #Find ceiling 
            if(float(rps) > rpsLeft and (leftRpsCeiling == -1 or (float(rps) - rpsLeft < float(rps) - leftRpsCeiling))):
                leftRpsCeiling = float(rps)
                leftPwmCeiling = pwm
        print("Foward Left RPS Floor: ", leftRpsFloor, "    Foward Left RPS Ceiling: ", leftRpsCeiling)

            
    
    else:  #backwards left
        rpsLeft *= -1 #make this positive for correct comparisions
        for rps, pwm in leftBwdSpeeds.items(): #uses pwm that results in backwards motion
            #Find floor
            if(float(rps) < rpsLeft and (leftRpsFloor == -1 or (rpsLeft - float(rps) < leftRpsFloor - float(rps)))):
                leftRpsFloor = float(rps)
                leftPwmFloor = pwm
                            #Find ceiling 
            if(float(rps) > rpsLeft and (leftRpsCeiling == -1 or (float(rps) - rpsLeft < float(rps) - leftRpsCeiling))):
                leftRpsCeiling = float(rps)
                leftPwmCeiling = pwm
        print("Backwords Left RPS Floor: ", leftRpsFloor, "     Left RPS Ceiling: ", leftRpsCeiling)
       
    
            
    if (rpsRight > 0):  #forwards right
        for rps, pwm in rightFwdSpeeds.items():
            #Find floor
            if(float(rps) < rpsRight and (rightRpsFloor == -1 or (rpsRight - float(rps) < rightRpsFloor - float(rps)))):
                rightRpsFloor = float(rps)
                rightPwmFloor = pwm

            #Find ceiling 
            if(float(rps) > rpsRight and (rightRpsCeiling == -1 or (float(rps) - rpsRight < float(rps) - rightRpsCeiling))):
                rightRpsCeiling = float(rps)
                rightPwmCeiling = pwm
        print("Foward Right RPS Floor: ", rightRpsFloor, "     Right RPS Ceiling: ", rightRpsCeiling)

        
    else:  #backwards right
        rpsRight *= -1 #make this positive for correct comparisons
        for rps, pwm in rightBwdSpeeds.items():  #uses pwm that results in backwards motion
            #Find floor
            if(float(rps) < rpsRight and (rightRpsFloor == -1 or (rpsRight - float(rps) < rightRpsFloor - float(rps)))):
                rightRpsFloor = float(rps)
                rightPwmFloor = pwm
                
            #Find ceiling 
            if(float(rps) > rpsRight and (rightRpsCeiling == -1 or (float(rps) - rpsRight < float(rps) - rightRpsCeiling))):
                rightRpsCeiling = float(rps)
                rightPwmCeiling = pwm
        print("Backwards Right RPS Floor: ", rightRpsFloor, "    Backwards Right RPS Ceiling: ", rightRpsCeiling)
                
        
    
    
    #Find the ratio between the two values, multiply desired rps by that for the PWM
    
#Set the speed based on inches per second
def setSpeedsIPS(ipsLeft, ipsRight):
    print("SetSpeedsIPS -- nothing here")
    #calculate the RPS required for this
    
    #call SetSpeedsRPS
    
#Set the speed of the robot so that the robot will move with a linear speed given by
#the parameter 'v' (in inches per second) with an angular velocity 'w' (radians per second)
#Positive angular velocities should make the robot spin counterclockwise
def setSpeedsvw(v, w):
    print("SetSpeedsvw -- nothing here");
    
    #I have no idea how we are supposed to use two velocities in the same robot, making a circle?

	
while False:
    # Write a maximum value of 1.7 for each servo.
    # Since the servos are oriented in opposite directions,
    # the robot will end up spinning in one direction.
    # Values between 1.3 and 1.7 should be used.
    
    
    pwm.set_pwm(LSERVO, 0, math.floor(1.6 / 20 * 4096))
    pwm.set_pwm(RSERVO, 0, math.floor(1.6 / 20 * 4096))
    time.sleep(4)
    print ("Speed: ", getSpeeds())
    pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096))
    pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096))

    print("Current Counts: ", lCount, " ", rCount)
    resetCounts()
    print("Previous counts: ", getCounts())
    print("Current Counts: ", lCount, " ", rCount)
    print ("Speed: ", getSpeeds())
    
    # Write a minimum value of 1.4 for each servo.
    # The robot will end up spinning in the other direction.
    pwm.set_pwm(LSERVO, 0, math.floor(1.4 / 20 * 4096))
    pwm.set_pwm(RSERVO, 0, math.floor(1.4 / 20 * 4096))
    time.sleep(4)
    
    print ("Speed: ", getSpeeds())
    time.sleep(10)
    print("Current Counts: ", lCount, " ", rCount)
    resetCounts()
    prev = getCounts()
    print("Current Counts: ", lCount, " ", rCount)
    print("Previous counts: ", prev)
    
    time.sleep(10)
	
initEncoders()
while True:
    calibrateSpeeds()
    x = 0.1
    while (x < 0.8):
        print("desired rpm: ", x)
        setSpeedsRPS(x, x)
        x+= 0.1
    x = -0.1
    while (x > -0.8):
        print("desired rpm: ", x)
        setSpeedsRPS(x, x)
        x-=0.1
    #print(leftSpeeds)
    #print(rightSpeeds)
    break
	
	
	
def StartFunction():
	initEncoders()
	calibrateSpeeds()
	
	while True:
		choice
		print("Welcome please choose from our options below: ")
		print("a = set speed via inches.")
		print("b = set speed via RPS.")
		print("c = set speed will set the general speed based on set of numbers still need to finish exactly which value this will pull.")
		print("e = exit program.")
		choice = raw_input("Please choose one and press enter!")
		if choice == "a":
			setSpeedsIPS()
		elif choice == "b":
			setSpeedsRPS()
		elif choice == "c":
			setSpeeds()
		elif choice == "e":
			break
		#could use a return statement here to end program will decide with you at lab
		else:
			print("Please choose a valid choice.")
	    
		
		