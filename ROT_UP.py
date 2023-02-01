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
            time.sleep(0.05) # add debouncing delay
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
            time.sleep(0.05) # add debouncing delay
