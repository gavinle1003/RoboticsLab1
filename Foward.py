import EncoderServo.py
#initialize our encoders and calibrate our speeds
initEncoders()
calibrateSpeeds()
#While true our program will run until user signals for exit
while True:
	#if user enters a q they will quit out of the program otherwise they will
	#keep entering values and moving our robot
	x = input("Press q to exit press enter to enter your values.")
	if x = 'q'
		break
		
	#if our input is to keep going we will get  our distance and time variables
	valueX = input("Enter the amount of inches youd like to go...")
	valueY = input("Enter the amount of time I have to complete this task!")
	#We will get our inches per second by dividing our distance by alloted time to
	#get avg velocity in inches per second
	IPS = valueX/valueY
	
	#need to make sure its possible before calling
	
	setSpeedIPS(IPS,IPS)

print("Closing program thank you!")

