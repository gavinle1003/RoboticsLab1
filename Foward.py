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

initEncoders()
calibrateSpeeds()
#While true our program will run until user signals for exit
while True:
	#if user enters a q they will quit out of the program otherwise they will
	#keep entering values and moving our robot
    x = input("Press q to exit press enter to enter your values.")
    if x == "q":
        break
		
	#if our input is to keep going we will get  our distance and time variables
    inputted_distance = input("Enter the amount of inches youd like to go...")
    inputted_time = input("Enter the amount of time I have to complete this task!")
	#We will get our inches per second by dividing our distance by alloted time to
	#get avg velocity in inches per second
    inputted_IPS = float(float(inputted_distance)/float(inputted_time))
    print("Inputted IPS: ", inputted_IPS)
	
	#to find possible IPS, find which is greater: the max speed for left wheel or right wheel
    if getMaxLeftFwd() >= getMaxRightFwd():
        possible_IPS = 2.61 * 3.14 * getMaxRightFwd()
    else:
        possible_IPS = 2.61 * 3.14 * getMaxLeftFwd()
        
    #Find the time and speed from user input and what is possible
    if inputted_IPS >= possible_IPS:
        print("Too fast for me, I'm going to do my best!")
        speed = possible_IPS
        go_time = float(inputted_distance)/possible_IPS
    else:
        speed = inputted_IPS
        go_time = float(inputted_distance)/inputted_IPS
            
    setSpeedsIPS(speed, speed)
    print(go_time)
    time.sleep(go_time)
    setSpeedsIPS(0,0)
	    
print("Closing program thank you!")

