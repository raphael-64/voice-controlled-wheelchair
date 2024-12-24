# This script uses the Vosk speech recognition library.
# Vosk is an open-source toolkit licensed under the Apache License 2.0.
# For more information, visit: https://alphacephei.com/vosk/

from vosk import Model, KaldiRecognizer
import pyaudio
import time
import os

model = Model("/Users/raphael/Documents/GitHub/voice-controlled-wheelchair/vosk-model")  #just my laptop, add the right path 
recognizer = KaldiRecognizer(model, 16000)

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()

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
            elif "turn right"  in text:
                turn_right()
except KeyboardInterrupt:
    print("\nProgram terminated by user")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("GPIO Cleaned Up")
