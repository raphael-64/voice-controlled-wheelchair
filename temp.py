import RPi.GPIO as GPIO
import time

# Left
PIN1_A = 29  # In1 A
PIN2_A = 31  # In2 A
ENA_A = 33   # PWM motor

# Right
PIN1_B = 40  # IN3 for Motor B
PIN2_B = 38  # IN4 for Motor B
ENA_B = 32   # PWM for Motor B

GPIO.setmode(GPIO.BOARD)  # Use Broadcom pin-numbering scheme

# Setup Motor A pins
GPIO.setup(PIN1_A, GPIO.OUT)
GPIO.setup(PIN2_A, GPIO.OUT)
GPIO.setup(ENA_A, GPIO.OUT)

# Setup Motor B pins
GPIO.setup(PIN1_B, GPIO.OUT)
GPIO.setup(PIN2_B, GPIO.OUT)
GPIO.setup(ENA_B, GPIO.OUT)

# Initialize PWM on ENA and ENB pins at 100Hz
pwm_a = GPIO.PWM(ENA_A, 100)  # Motor A PWM
pwm_b = GPIO.PWM(ENA_B, 100)  # Motor B PWM

pwm_a.start(75)
pwm_b.start(75)

# Move forward
GPIO.output(PIN1_A, GPIO.HIGH)
GPIO.output(PIN2_A, GPIO.LOW)
GPIO.output(PIN1_B, GPIO.HIGH)
GPIO.output(PIN2_B, GPIO.LOW)

# Wait for 5 seconds
time.sleep(5)

# Stop the motors
GPIO.output(PIN1_A, GPIO.LOW)
GPIO.output(PIN2_A, GPIO.LOW)
GPIO.output(PIN1_B, GPIO.LOW)
GPIO.output(PIN2_B, GPIO.LOW)

# Cleanup
pwm_a.stop()
pwm_b.stop()
GPIO.cleanup()