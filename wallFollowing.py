
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


for count in range(1, 100):
    # Get a measurement from each sensor
    lDistance = lSensor.get_distance()
    fDistance = fSensor.get_distance()
    rDistance = rSensor.get_distance()
    
    # Print each measurement
    print("Left: {}\tFront: {}\tRight: {}".format(lDistance, fDistance, rDistance))

# Stop measurement for all sensors
lSensor.stop_ranging()
fSensor.stop_ranging()
rSensor.stop_ranging()
