import pigpio
import time
import math

# Function to generate a sine wave using PWM
def sine_wave(pi, gpio_pin, frequency, amplitude, duration):
    period = 1.0 / frequency
    steps = 100
    step_time = period / steps
    
    pi.set_PWM_frequency(gpio_pin, int(steps / period))
    start_time = time.time()

    while time.time() - start_time < duration:
        for step in range(steps):
            duty_cycle = int(amplitude * (1 + math.sin(2 * math.pi * step / steps)))
            pi.set_PWM_dutycycle(gpio_pin, duty_cycle)
            time.sleep(step_time)

# Initialize pigpio
pi = pigpio.pi()

# Define the GPIO pin
gpio_pin = 18

# Set the GPIO pin as output
pi.set_mode(gpio_pin, pigpio.OUTPUT)

# Generate a sine wave with the following parameters:
# frequency: 100 Hz, amplitude: 128, duration: 5 seconds
sine_wave(pi, gpio_pin, 100, 128, 5)

# Cleanup
pi.stop()
