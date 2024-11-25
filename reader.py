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

pwm_a.start(100)
pwm_b.start(100)

try:
    while(True):
        user_input = input()
        print("Input: " +user_input)
        if user_input == "go\n":    
            GPIO.output(PIN1_A, GPIO.HIGH)
            GPIO.output(PIN2_A, GPIO.LOW)
            
            GPIO.output(PIN1_B, GPIO.HIGH)
            GPIO.output(PIN2_B, GPIO.LOW)
            time.sleep(2)
            print("go")

        elif user_input == "back\n":
            GPIO.output(PIN1_A, GPIO.LOW)
            GPIO.output(PIN2_A, GPIO.HIGH)
            
            GPIO.output(PIN1_B, GPIO.LOW)
            GPIO.output(PIN2_B, GPIO.HIGH)

        elif user_input == "left\n": 
            GPIO.output(PIN1_A, GPIO.LOW)
            GPIO.output(PIN2_A, GPIO.HIGH)
                
            GPIO.output(PIN1_B, GPIO.HIGH)
            GPIO.output(PIN2_B, GPIO.LOW)

        elif user_input == "right\n":
            GPIO.output(PIN1_A, GPIO.HIGH)
            GPIO.output(PIN2_A, GPIO.LOW)
        
            GPIO.output(PIN1_B, GPIO.LOW)
            GPIO.output(PIN2_B, GPIO.HIGH)

except user_input == "stop":
    GPIO.output(PIN1_A, GPIO.LOW)
    GPIO.output(PIN2_A, GPIO.LOW)
        
    GPIO.output(PIN1_B, GPIO.LOW)
    GPIO.output(PIN2_B, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
