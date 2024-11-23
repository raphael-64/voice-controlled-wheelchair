import os
import RPi.GPIO as GPIO
import time

# Left
PIN1_A = 29 #In1 A
PIN2_A = 31 #in2 A
ENA_A = 33 #PWM motor

# Right
PIN1_B = 40   # IN3 for Motor B
PIN2_B = 38   # IN4 for Motor B
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

pwm_a.start(0)
pwm_b.start(0)

speed_a = 50  # Motor A speed
speed_b = 50  # Motor B speed

input = open("output.txt").read()
print("Input:" + input + "n")

def update_speed():
    pwm_a.ChangeDutyCycle(speed_a)
    pwm_b.ChangeDutyCycle(speed_b)

if input == "go\n":
    GPIO.output(PIN1_A, GPIO.HIGH)
    GPIO.output(PIN2_A, GPIO.LOW)
    
    GPIO.output(PIN1_B, GPIO.HIGH)
    GPIO.output(PIN2_B, GPIO.LOW)
    update_speed()

elif input == "back\n":
    GPIO.output(PIN1_A, GPIO.LOW)
    GPIO.output(PIN2_A, GPIO.HIGH)
    
    GPIO.output(PIN1_B, GPIO.LOW)
    GPIO.output(PIN2_B, GPIO.HIGH)
    update_speed()

elif input == "left\n": 
    GPIO.output(PIN1_A, GPIO.LOW)
    GPIO.output(PIN2_A, GPIO.HIGH)
        
    GPIO.output(PIN1_B, GPIO.HIGH)
    GPIO.output(PIN2_B, GPIO.LOW)
    update_speed()

elif input == "right\n":
    GPIO.output(PIN1_A, GPIO.HIGH)
    GPIO.output(PIN2_A, GPIO.LOW)
   
    GPIO.output(PIN1_B, GPIO.LOW)
    GPIO.output(PIN2_B, GPIO.HIGH)
    update_speed()

elif input == "down":
    speed_a = max(speed_a - 10, 0)
    speed_b = max(speed_b - 10, 0)

elif input == "up":
    speed_a = min(speed_a + 10, 100)
    speed_b = min(speed_b + 10, 100)

elif input == "stop\n":
    GPIO.output(PIN1_A, GPIO.LOW)
    GPIO.output(PIN2_A, GPIO.LOW)
        
    GPIO.output(PIN1_B, GPIO.LOW)
    GPIO.output(PIN2_B, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()


