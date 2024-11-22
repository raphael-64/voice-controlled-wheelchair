from vosk import Model, KaldiRecognizer
import pyaudio
import RPi.GPIO as GPIO
import time

# Left
PIN1_A = 22 #In1 A
PIN2_A = 21 #in2 A
ENA_A = 23 #PWM motor

# Right
PIN1_B = 27   # IN3 for Motor B
PIN2_B = 11   # IN4 for Motor B
ENA_B = 26   # PWM for Motor B

GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme

# Setup Motor A pins
GPIO.setup(PIN1_A, GPIO.OUT)
GPIO.setup(PIN2_A, GPIO.OUT)
GPIO.setup(ENA_A, GPIO.OUT)

# Setup Motor B pins
GPIO.setup(PIN1_B, GPIO.OUT)
GPIO.setup(PIN2_B, GPIO.OUT)
GPIO.setup(ENA_B, GPIO.OUT)


model = Model("/Users/raphael/Documents/Github/voice-controlled-wheelchair/vosk-model")  #just my laptop, add the right path 
recognizer = KaldiRecognizer(model, 16000)

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()

# Initialize PWM on ENA and ENB pins at 100Hz
pwm_a = GPIO.PWM(ENA_A, 100)  # Motor A PWM
pwm_b = GPIO.PWM(ENA_B, 100)  # Motor B PWM

# Start PWM with 0% duty cycle (motors stopped)
pwm_a.start(0)
pwm_b.start(0)


speed_a = 50  # Motor A speed
speed_b = 50  # Motor B speed

def update_speed():
    pwm_a.ChangeDutyCycle(speed_a)
    pwm_b.ChangeDutyCycle(speed_b)


def go_forward():
    GPIO.output(PIN1_A, GPIO.HIGH)
    GPIO.output(PIN2_A, GPIO.LOW)
    
    GPIO.output(PIN1_B, GPIO.HIGH)
    GPIO.output(PIN2_B, GPIO.LOW)
    
    update_speed()
    print("Command: Go Forward")

def go_backward():
    GPIO.output(PIN1_A, GPIO.LOW)
    GPIO.output(PIN2_A, GPIO.HIGH)
    
    GPIO.output(PIN1_B, GPIO.LOW)
    GPIO.output(PIN2_B, GPIO.HIGH)
    
    update_speed()
    print("Command: Go Backward")
    

def stop_motors():
    GPIO.output(PIN1_A, GPIO.LOW)
    GPIO.output(PIN2_A, GPIO.LOW)
    
    GPIO.output(PIN1_B, GPIO.LOW)
    GPIO.output(PIN2_B, GPIO.LOW)
    
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    print("Command: Stop Motors")

def turn_left():
    GPIO.output(PIN1_A, GPIO.HIGH)
    GPIO.output(PIN2_A, GPIO.LOW)
    
    GPIO.output(PIN1_B, GPIO.LOW)
    GPIO.output(PIN2_B, GPIO.HIGH)
    
    update_speed()
    print("Command: Turn Left")

def turn_right():
    GPIO.output(PIN1_A, GPIO.LOW)
    GPIO.output(PIN2_A, GPIO.HIGH)
    
    GPIO.output(PIN1_B, GPIO.HIGH)
    GPIO.output(PIN2_B, GPIO.LOW)
    
    update_speed()
    print("Command: Turn Right")

def slow_down():
    global speed_a, speed_b
    # Decrease speed by 10%, ensuring it doesn't go below 0%
    speed_a = max(speed_a - 10, 0)
    speed_b = max(speed_b - 10, 0)
    update_speed()

def speed_up():
    global speed_a, speed_b
    # Increase speed by 10%, ensuring it doesn't exceed 100%
    speed_a = min(speed_a + 10, 100)
    speed_b = min(speed_b + 10, 100)
    update_speed()

try:
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = eval(result)["text"]

            if "go" in text:
                go_forward()
            elif "back" in text:
                go_backward()
            elif "stop" in text:
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
    GPIO.cleanup()
    print("GPIO Cleaned Up")
