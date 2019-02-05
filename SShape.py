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


