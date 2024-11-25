from vosk import Model, KaldiRecognizer
import pyaudio
import time
import socket
import subprocess
import os

model = Model("/Users/steph/OneDrive/Documents/Coding/SE101/voice-controlled-wheelchair/vosk_env/vosk-model")  #just my laptop, add the right path 
recognizer = KaldiRecognizer(model, 16000)
IPAdd = "192.168.124.29"
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, input_device_index=3, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()


# Define server address and port
SERVER_IP = ''  # Replace with Raspberry Pi's IP address
SERVER_PORT = 1200

# Message to send
current_state = "stop"

def update_state(new_state):
    global current_state
    if new_state != current_state:
        if new_state == "go":
            os.system("python3 ./commands/go.py| nc "+IPAdd+" 1200")
            print("go")
        elif new_state == "back":
            os.system("python3 ./commands/back.py | nc "+IPAdd+" 1200")
            print("back")
        elif new_state == "stop":
            os.system("python3 ./commands/stop.py | nc "+IPAdd+" 1200")
            print("stop")
        elif new_state == "turn left":
            os.system("python3 ./commands/left.py | nc "+IPAdd+" 1200")
            print("left")
        elif new_state == "turn right":
            os.system("python3 ./commands/right.py| nc "+IPAdd+" 1200")
            print("turn right")

try:
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = eval(result)["text"]
            if "go" in text:
                update_state("go")
            elif "back" in text:
                update_state("back")
            elif "stop" in text:
                update_state("stop")
            elif "turn left" in text:
                update_state("left")
            elif "turn right" in text:
                update_state("turn right")


except KeyboardInterrupt:
    print("\nProgram terminated by user")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
