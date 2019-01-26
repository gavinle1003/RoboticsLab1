# This program demonstrates usage of the servos.
# Keep the robot in a safe location before running this program,
# as it will immediately begin moving.
# See https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/ for more details.

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
leftSpeeds = {'0.0':'1.5'}
rightSpeeds = {'0.0':'1.5'}

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
    for i in range(130, 151):
        x = float(i/100)
        startTime = time.time()
        pwm.set_pwm(LSERVO, 0, math.floor(x / 20 * 4096))
        pwm.set_pwm(RSERVO, 0, math.floor(x / 20 * 4096))
        time.sleep(1)
        #gets speeds of wheels after it changes we will need to add in time wait for the specified number of seconds.
	#along with a 1 second interval
        y = getSpeeds()
        resetCounts()

	#each time we get these speeds we will enter the values into our dictionary
	#this will make it easier to print our graph
        leftSpeeds[y[0]] = x
        
        print("Left wheel speed: ", leftSpeeds[y[0]], " RPS: ", y[0])
    
    #Calibrate Right Wheel
    for j in range(150, 171):
        x = float(j/100)
        startTime = time.time()
        pwm.set_pwm(LSERVO, 0, math.floor(x / 20 * 4096))
        pwm.set_pwm(RSERVO, 0, math.floor(x / 20 * 4096))
        time.sleep(1)

        y = getSpeeds()
        resetCounts()

        rightSpeeds[y[1]] = x
        
        print("Right wheel speed: ", rightSpeeds[y[1]], " RPS: ", y[1])

    pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096))
    pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096))

 
#Set the speed of the motors based on RPS
def setSpeedsRPS(rpsLeft, rpsRight):
    print("SetSpeedsRPS -- nothing here")
    #Find the speed in the dictionary closest to the inputted balue
    
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
    print(leftSpeeds)
    print(rightSpeeds)
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
	    
		
		