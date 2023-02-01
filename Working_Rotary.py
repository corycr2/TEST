import RPi.GPIO as GPIO
import time

clk = 18
dt = 23
sw = 24
# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP) #clk
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP) #dt
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP) #sw
previousValue = 1
resistance = 0
prev_time = time.time()

def rotary_active():
    global previousValue
    global resistance
    global prev_time
    current_time = time.time()
    if previousValue != GPIO.input(clk):
        if GPIO.input(clk) == 0:
            if GPIO.input(dt) == 0:
                direction = "anti-clockwise"
                speed = current_time - prev_time
                if speed < .2:
                    if (resistance - 100) > 100:
                        resistance -= 100
                    else:
                        resistance = 100
                elif (resistance - 10) > 100:
                    resistance -= 10
                else:
                    resistance = 100
                print(f"Direction: {direction}, Resistance: {resistance}, Speed: {speed}")
                time.sleep(.1)
                prev_time = current_time
            else:
                direction = "clockwise"
                speed = current_time - prev_time
                if speed < .2:
                    if (resistance + 100) < 10000:
                        resistance += 100
                    else:
                        resistance = 10000
                elif (resistance + 10) < 10000:
                    resistance += 10
                else:
                    resistance = 10000
                print(f"Direction: {direction}, Resistance: {resistance}, Speed: {speed}")
                time.sleep(.1)
                prev_time = current_time                
        previousValue = GPIO.input(clk)
         
while True:
    prev_time = time.time()
    while GPIO.input(sw) == 0:
        if (prev_time - time.time()) > 3:
            count = 1
            print("Editing mode")
            time.sleep(.5)
    while count == 1:
        rotary_active()
        prev_time = time.time()
        while GPIO.input(sw) == 0:
            if (prev_time - time.time()) > 3:
                print(f"Final resistance is : {resistance}")
                time.sleep(.5)
                count = 0
      
    