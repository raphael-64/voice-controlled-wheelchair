import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme

# Left
PIN1_A = 22 #In1 A
PIN2_A = 21 #in2 A
ENA_A = 23 #PWM motor

# Right
PIN1_B = 27   # IN3 for Motor B
PIN2_B = 11   # IN4 for Motor B
ENA_B = 26   # PWM for Motor B

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

GPIO.output(PIN1_A, GPIO.HIGH)
GPIO.output(PIN2_A, GPIO.LOW)
   
GPIO.output(PIN1_B, GPIO.HIGH)
GPIO.output(PIN2_B, GPIO.LOW)

pwm_a.ChangeDutyCycle(50)
pwm_b.ChangeDutyCycle(50)

