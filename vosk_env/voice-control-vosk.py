from vosk import Model, KaldiRecognizer
import pyaudio
import time
import os

import sys
import queue
import sounddevice as sd
import json 
import subprocess

# Left
PIN1_A = 21 #In1 A
PIN2_A = 22 #in2 A
ENA_A = 23 #PWM motor

# Right
PIN1_B = 29   # IN3 for Motor B
PIN2_B = 28   # IN4 for Motor B
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

audio_queue = queue.Queue()
def audio_callback(indata, frames, time, status):
    audio_queue.put(bytes(indata))

def get_blackhole_device_index():
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        if 'Blackhole' in device['name']:
            return idx


def main():
    print("Starting audio stream...")
    try:
        # Open the input stream
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                               channels=0, callback=audio_callback,
                               device=BLACKHOLE_DEVICE_INDEX):
            print("Listening... Press Ctrl+C to stop.")
            while True:
                data = audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    text = json.loads(result).get("text", "")
                    if text:
                        print(f"Recognized: {text}")
                else:
                    partial = recognizer.PartialResult()
                    partial_text = json.loads(partial).get("partial", "")
                    if partial_text:
                        print(f"Partial: {partial_text}", end='\r')
    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        BLACKHOLE_DEVICE_INDEX = get_blackhole_device_index()
    except ValueError as e:
        print(e)
        sys.exit(1)
    
    main()


model = Model("/Users/richardhuang/Documents/GitHub/se101project-voiceControlledWheelchair/vosk_env/vosk-model")  #just my laptop, add the right path 
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
