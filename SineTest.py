import math
import time
from gpiozero import OutputDevice

def generate_sine_wave(frequency, amplitude, duration, resolution=8):
    step_size = (2 * math.pi) / (2 ** resolution)
    sine_wave = []
    for i in range(2 ** resolution):
        value = math.sin(i * step_size)
        sine_wave.append(int(((value + 1) * amplitude) / 2))
    return sine_wave

def main():
    gpio_pins = [2, 3, 4, 14, 15, 18, 17, 27]  # BCM pin numbers
    output_devices = [OutputDevice(pin) for pin in gpio_pins]
    resolution = 8
    duration = 1

    while True:
        frequency = float(input("Enter frequency (1kHz-10kHz): ")) * 1000
        amplitude = float(input("Enter amplitude (0-5V): ")) / 5
        sine_wave = generate_sine_wave(frequency, amplitude, duration, resolution)

        start_time = time.time()
        while time.time() - start_time < duration:
            for value in sine_wave:
                for bit in range(resolution):
                    if value & (1 << bit):
                        output_devices[bit].on()
                    else:
                        output_devices[bit].off()
                time.sleep(1 / (frequency * (2 ** resolution)))

if __name__ == "__main__":
    main()
