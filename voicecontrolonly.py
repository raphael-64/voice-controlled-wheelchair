from vosk import Model, KaldiRecognizer
import pyaudio
import time
import socket
import subprocess
import os

model = Model("/Users/richardhuang/Documents/GitHub/se101project-voiceControlledWheelchair/vosk_env/vosk-model")  #just my laptop, add the right path 
recognizer = KaldiRecognizer(model, 16000)
IPAdd = "192.168.124.29"
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, input_device_index=3, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()


# Define server address and port
SERVER_IP = '172.20.10.2'  # Replace with Raspberry Pi's IP address
SERVER_PORT = 65432

# Message to send
MESSAGE = 'go'


try:
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = eval(result)["text"]

            if "go" in text:
                os.system("python3 ./commands/go.py| nc "+IPAdd+" 1200")
                print("go")
            elif "back" in text:
                os.system("python3 ./commands/back.py | nc "+IPAdd+" 1200")
                print("back")
            elif "stop" in text:
                os.system("python3 ./commands/stop.py | nc "+IPAdd+" 1200")
                print("stop")
            elif "turn left" in text:
                os.system("python3 ./commands/left.py | nc "+IPAdd+" 1200")
                print("left")
            elif "turn right" in text:
                os.system("python3 ./commands/right.py| nc "+IPAdd+" 1200")
                print("turn right")
            elif "slow down" in text:
                os.system("python3 ./commands/down.py | nc "+IPAdd+" 1200")
                print("down")
            elif "speed up" in text:
                os.system("python3 ./commands/up.py| nc "+IPAdd+" 1200")
                print("up")
            elif "destroy" in text:
                os.system("python3 ./commands/destroy.py | nc "+IPAdd+" 1200")
                print("destroy")
except KeyboardInterrupt:
    print("\nProgram terminated by user")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
