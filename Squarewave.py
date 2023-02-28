#import all functions to be used
import sys
sys.path.append('../')
import rgb1602
import RPi.GPIO as GPIO
import time
import pigpio 

#This creates the interface to talk to the digital potentiometer
pi1 = pigpio.pi()
h = pi1.spi_open(1,97600)


offset_resistance = 0
height_voltage = 0
voltage = 0



GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

pwm = GPIO.PWM(21, 1000) # 1 kHz frequency
pwm.start(100) # 100% duty cycle

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()
