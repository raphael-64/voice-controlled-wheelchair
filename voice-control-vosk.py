from vosk import Model, KaldiRecognizer
import pyaudio
import RPi.GPIO as GPIO
import time

# Motor A
PIN1_A = 23 #In1 A
PIN2_A = 24 #in2 A
ENA_A = 18 #PWM motor

# Motor B
PIN1_B = 8   # IN3 for Motor B
PIN2_B = 7   # IN4 for Motor B
ENA_B = 25   # PWM for Motor B

# Motor C
PIN1_C = 16  # IN1 for Motor C
PIN2_C = 20  # IN2 for Motor C
ENA_C = 12   # PWM for Motor C

# Motor D
PIN1_D = 19  # IN3 for Motor D
PIN2_D = 26  # IN4 for Motor D
ENA_D = 21   # PWM for Motor D

GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme

# Setup Motor A pins
GPIO.setup(PIN1_A, GPIO.OUT)
GPIO.setup(PIN2_A, GPIO.OUT)
GPIO.setup(ENA_A, GPIO.OUT)

# Setup Motor B pins
GPIO.setup(PIN1_B, GPIO.OUT)
GPIO.setup(PIN2_B, GPIO.OUT)
GPIO.setup(ENA_B, GPIO.OUT)

# Setup Motor C pins
GPIO.setup(PIN1_C, GPIO.OUT)
GPIO.setup(PIN2_C, GPIO.OUT)
GPIO.setup(ENA_C, GPIO.OUT)

# Setup Motor D pins
GPIO.setup(PIN1_D, GPIO.OUT)
GPIO.setup(PIN2_D, GPIO.OUT)
GPIO.setup(ENA_D, GPIO.OUT)

model = Model("/Users/raphael/Documents/Github/voice-controlled-wheelchair/vosk-model")  #just my laptop, add the right path 
recognizer = KaldiRecognizer(model, 16000)

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()

# Initialize PWM on ENA and ENB pins at 100Hz
pwm_a = GPIO.PWM(ENA_A, 100)  # Motor A PWM
pwm_b = GPIO.PWM(ENA_B, 100)  # Motor B PWM
pwm_c = GPIO.PWM(ENA_C, 100)  # Motor C PWM
pwm_d = GPIO.PWM(ENA_D, 100)  # Motor D PWM

# Start PWM with 0% duty cycle (motors stopped)
pwm_a.start(0)
pwm_b.start(0)
pwm_c.start(0)
pwm_d.start(0)

speed_a = 50  # Motor A speed
speed_b = 50  # Motor B speed
speed_c = 50  # Motor C speed
speed_d = 50  # Motor D speed

def update_speed():
    pwm_a.ChangeDutyCycle(speed_a)
    pwm_b.ChangeDutyCycle(speed_b)
    pwm_c.ChangeDutyCycle(speed_c)
    pwm_d.ChangeDutyCycle(speed_d)

def go_forward():
    GPIO.output(PIN1_A, GPIO.HIGH)
    GPIO.output(PIN2_A, GPIO.LOW)
    
    GPIO.output(PIN1_B, GPIO.HIGH)
    GPIO.output(PIN2_B, GPIO.LOW)
    
    GPIO.output(PIN1_C, GPIO.HIGH)
    GPIO.output(PIN2_C, GPIO.LOW)
    
    GPIO.output(PIN1_D, GPIO.HIGH)
    GPIO.output(PIN2_D, GPIO.LOW)
    
    update_speed()
    print("Command: Go Forward")

def stop_motors():
    GPIO.output(PIN1_A, GPIO.LOW)
    GPIO.output(PIN2_A, GPIO.LOW)
    
    GPIO.output(PIN1_B, GPIO.LOW)
    GPIO.output(PIN2_B, GPIO.LOW)
    
    GPIO.output(PIN1_C, GPIO.LOW)
    GPIO.output(PIN2_C, GPIO.LOW)
    
    GPIO.output(PIN1_D, GPIO.LOW)
    GPIO.output(PIN2_D, GPIO.LOW)
    
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    pwm_c.ChangeDutyCycle(0)
    pwm_d.ChangeDutyCycle(0)
    print("Command: Stop Motors")

def turn_left():
    GPIO.output(PIN1_A, GPIO.HIGH)
    GPIO.output(PIN2_A, GPIO.LOW)
    
    GPIO.output(PIN1_B, GPIO.HIGH)
    GPIO.output(PIN2_B, GPIO.LOW)
    
    GPIO.output(PIN1_C, GPIO.LOW)
    GPIO.output(PIN2_C, GPIO.HIGH)
    
    GPIO.output(PIN1_D, GPIO.LOW)
    GPIO.output(PIN2_D, GPIO.HIGH)
    
    update_speed()
    print("Command: Turn Left")

def turn_right():
    GPIO.output(PIN1_A, GPIO.LOW)
    GPIO.output(PIN2_A, GPIO.HIGH)
    
    GPIO.output(PIN1_B, GPIO.LOW)
    GPIO.output(PIN2_B, GPIO.HIGH)
    
    GPIO.output(PIN1_C, GPIO.HIGH)
    GPIO.output(PIN2_C, GPIO.LOW)
    
    GPIO.output(PIN1_D, GPIO.HIGH)
    GPIO.output(PIN2_D, GPIO.LOW)
    
    update_speed()
    print("Command: Turn Right")

def slow_down():
    global speed_a, speed_b, speed_c, speed_d
    # Decrease speed by 10%, ensuring it doesn't go below 0%
    speed_a = max(speed_a - 10, 0)
    speed_b = max(speed_b - 10, 0)
    speed_c = max(speed_c - 10, 0)
    speed_d = max(speed_d - 10, 0)
    update_speed()

def speed_up():
    global speed_a, speed_b, speed_c, speed_d
    # Increase speed by 10%, ensuring it doesn't exceed 100%
    speed_a = min(speed_a + 10, 100)
    speed_b = min(speed_b + 10, 100)
    speed_c = min(speed_c + 10, 100)
    speed_d = min(speed_d + 10, 100)
    update_speed()

try:
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = eval(result)["text"]
            init()

            if "go" in text:
                # activate GPIO for forward motion
                go_forward()
            elif "stop" in text:
                # GPIO for stop
                stop_motors()
            elif "turn left" in text:
                turn_left()
            elif "turn right" in text:
                turn_right()
            elif "slow down" in text:
                slow_down()
            elif "speed up" in text:
                speed_up()
except KeyboardInterrupt:
    print("\nProgram terminated by user")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    pwm_a.stop()
    pwm_b.stop()
    pwm_c.stop()
    pwm_d.stop()
    GPIO.cleanup()
    print("GPIO Cleaned Up")
