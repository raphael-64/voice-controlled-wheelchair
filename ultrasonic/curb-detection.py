import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 8
ECHO = 9

print("Distance measurement in progress...")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:
    GPIO.output(TRIG, False)
    print("Waiting for sensor to settle...")
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    pulse_end = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = round(pulse_duration * 17150, 2)

    print("Distance: ", distance, "cm")

finally:
    GPIO.cleanup()
