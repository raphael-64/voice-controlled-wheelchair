from vosk import Model, KaldiRecognizer
import pyaudio
import RPi.GPIO as GPIO
import time
import os

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


model = Model("/Users/raphael/Documents/Coding/SE101/voice-controlled-wheelchair/vosk-model")  #just my laptop, add the right path 
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

def go_forward():
    os.system("python forward.py")

def go_backward():
    os.system("python backward.py")
    

def stop_motors():
    os.system("python stop.py")

def turn_left():
    os.system("python left.py")

def turn_right():
    os.system("python right.py")


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
