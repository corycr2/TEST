import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up event detection for both channels
GPIO.add_event_detect(18, GPIO.BOTH, bouncetime=2)
GPIO.add_event_detect(23, GPIO.BOTH, bouncetime=2)

def rotary_callback(channel):
    current_time = time.time()
    global prev_time
    global prev_state
    global resistance
    state = GPIO.input(channel)
    if channel == 18:
        if state != prev_state[0]:
            if state == 0:
                direction = "Clockwise"
                speed = current_time - prev_time
                if speed < 0.01:
                    resistance += 100
                else:
                    resistance += 1
            else:
                direction = "Counterclockwise"
                speed = current_time - prev_time
                if speed < 0.01:
                    resistance -= 100
                else:
                    resistance -= 1
            print(f"Direction: {direction}, Speed: {speed}, Resistance: {resistance}")
            prev_time = current_time
            prev_state[0] = state
    else:
        if state != prev_state[1]:
            if state == 0:
                direction = "Clockwise"
                speed = current_time - prev_time
                if speed < 0.01:
                    resistance += 100
                else:
                    resistance += 1
            else:
                direction = "Counterclockwise"
                speed = current_time - prev_time
                if speed < 0.01:
                    resistance -= 100
                else:
                    resistance -= 1
            print(f"Direction: {direction}, Speed: {speed}, Resistance: {resistance}")
            prev_time = current_time
            prev_state[1] = state


prev_state = [1, 1]
prev_time = time.time()

# Add the callback function for both channels
GPIO.add_event_callback(18, rotary_callback)
GPIO.add_event_callback(23, rotary_callback)

resistance = 0
# Keep the program running
while True:
    time.sleep
