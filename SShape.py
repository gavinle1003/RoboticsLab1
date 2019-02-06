<<<<<<< HEAD
from EncoderServo import initEncoders
from EncoderServo import calibrateSpeeds
from EncoderServo import setSpeedsIPS
from EncoderServo import setSpeedsvw
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
#initialize our encoders and calibrate our speeds
initEncoders()
calibrateSpeeds()
#Start our loop in order to keep running until the user would like to exit
while True:
    x = input("Press q to exit or press enter when ready to start entering values!")
    if x == 'q':
        break
#when we continute we will record our radius and time constraints each time
#for our two semi-circles
    UserRadius1 = input("Enter Radius 1 and press enter:")
    UserRadius2 = input("Enter Radius 2 and press enter:")
    UserTime = input("Enter the number of seconds I have to complete this task: ")
    
#Calculates our circumference for both of our Radius values
    Circumference1 = 2 * 3.14 * float(UserRadius1)
    Circumference2 = 2 * 3.14 * float(UserRadius2)

#Divide this by 2 in order to get our 2 travel distances since we are going half a circle each time
    TravelDistance1 = float(Circumference1)/2.0
    TravelDistance2 = float(Circumference2)/2.0
    TotalTravelDistance = TravelDistance1 + TravelDistance2

#Next we get our velocity by dividing our distance by requested time for each semi circle
    Velocity = float(TotalTravelDistance)/float(UserTime)


#We calculate our angular velocity value for each semi circle
    AngularVelocity1 = float(Velocity)/float(UserRadius1)
    AngularVelocity2 = float(Velocity)/float(UserRadius2)

#Need to do a loop for each of these set speeds because they are both a different circle
    
    #Find max speed for going clockwise by calculating the speed of the left wheel
    LVelocity = AngularVelocity1 * float(UserRadius1)
    
    #Check for clockwise max speed with left wheel max speed
    if LVelocity > (getMaxLeftFwd()* 2.61 * 3.14):
        print("Too fast for me for the first semicircle, I'm going to do my best!")
        go_velocity1 = getMaxLeftFwd() * 2.61 * 3.14
        go_time1 = float(TravelDistance1)/go_velocity1
    else:
        go_velocity1 = LVelocity
        go_time1 = float(TravelDistance1)/go_velocity1
        

    #Find max speed for going clockwise by calculating the speed of the right wheel
    RVelocity = AngularVelocity2 * float(UserRadius2)

    #Check for counterclockwise max speed with right wheel max speed
    if RVelocity > (getMaxRightFwd()* 2.61 * 3.14):
        print("Too fast for me for the second semicircle, I'm going to do my best!")
        go_velocity2 = getMaxRightFwd() * 2.61 * 3.14
        go_time2 = float(TravelDistance2)/go_velocity2
    else:
        go_velocity2 = RVelocity
        go_time2 = float(TravelDistance2)/go_velocity2
    
    #set the angular Velocities
    go_angular1 = (float(go_velocity1)/float(UserRadius1)) * -1
    go_angular2 = float(go_velocity2)/float(UserRadius2)
    
    setSpeedsvw(go_velocity1, go_angular1)  #clockwise is negative
    time.sleep(go_time1)
    print(go_time1)
    setSpeedsIPS(0,0)
    time.sleep(1)
    setSpeedsvw(go_velocity2, go_angular2)
    time.sleep(go_time2)
    print(go_time2)
    setSpeedsIPS(0, 0)
print("Closing program thank you!")

	
   

=======
import EncoderServo.py
#initialize our encoders and calibrate our speeds
initEncoders()
calibrateSpeeds()
#Start our loop in order to keep running until the user would like to exit
while True:
	x = input("Press q to exit or press enter when ready to start entering values!")
	if x = 'q'
		break
	#when we continute we will record our radius and time constraints each time
	#for our two semi-circles
	valueR1 = input("Enter Radius 1 and press enter:")
	time1 = input("Enter the number of seconds I have to complete this task: ")
	valueR2 = input("Enter Radius 2 and press enter:")
	time2 = input("Enter the number of seconds I have to complete this task and press enter: ")
	#Calculates our circumference for both of our Radius values
	Circumference1 = 2 * 3.14 * valueR1
	Circumference2 = 2 * 3.14 * valueR2

	#Divide this by 2 in order to get our 2 travel distances
	TravelDistance1 = Circumference1/2
	TravelDistance2 = Circumference2/2

#Next we get our velocity by dividing our distance by requested time for each semi circle
	V1 = TravelDistance1/time1
	V2 = TravelDistance2/time2

#This will calculate the travel time for a "perfect" run with these values
	TravelTime1 = TravelDistance1/V1
	TravelTime2 = TravelDistance2/V2

#If the needed travel time is more then the requested we know this isnt possible and will do it as fast as possible
#Need to finish constraints for our conditions
	if TravelTime > time1 or TravelTime2 > time2:
		print("The travel time isnt possible I will go as fast as possible!")

#We calculate our angular velocity value for each semi circle
	W1 = valueR1/V1
	W2 = valueR2/V2

#We then set our speeds for the semi-circle by plugging our Velocity
#and our angular velocity into our function
	setSpeedIPS(V1,W1)
	setSpeedIPS(V2,W2)


>>>>>>> 76397da5345159091bf99d4b52ae31fec9fdbf08
