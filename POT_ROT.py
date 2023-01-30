
import pigpio
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO.setup(18, GPIO.OUT)
GPIO.setup(25, GPIO.IN) #THIS WILL BE ROTARY ENCODER CLK 
GPIO.setup(24, GPIO.IN) #THIS WILL BE ROTARY ENCODER DT
GPIO.setup(23, GPIO.IN) #THIS WILL BE ROTARY ENCODER PRESS

count = 0

while True:
    if GPIO.input(25) == 0:
        time.sleep(0.5) #This should account for debounce may want to increase debounce time
        count += 1
    if count%2 != 0:
        GPIO.output(18, GPIO.HIGH)
        #add anything you want to do after the button on the encoder is pressed
    else:
        GPIO.output(18, GPIO.LOW)
        
    
        # Should not need this if the button is not pressed // time.sleep(0.5) #This should account for debounce


GPIO.cleanup()






