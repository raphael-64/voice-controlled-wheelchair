from vosk import Model, KaldiRecognizer
import pyaudio
import time
import socket
import subprocess
import os


# Get the user identifier from the environment
user = os.getenv('USER')  # For macOS/Linux, or use 'USERNAME' for Windows

if user == "richardhuang":
    model_path = "/Users/richardhuang/Documents/GitHub/voice-controlled-wheelchair/vosk_env/vosk-model"
    input_device_index = 3
elif user == "raphael":
    model_path = "/Users/raphael/Documents/GitHub/voice-controlled-wheelchair/vosk_env/vosk-model"
    input_device_index = 0
else:
    raise ValueError("Unrecognized user or system configuration.")

# Initialize the model and audio stream
model = Model(model_path)

recognizer = KaldiRecognizer(model, 16000)
IP = "192.168.40.29"
audio = pyaudio.PyAudio()

stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    input_device_index=input_device_index,
    rate=16000,
    input=True,
    frames_per_buffer=4096
)

stream.start_stream()

try:
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = eval(result)["text"]

            if "go" in text:
                os.system("python3 ./commands/go.py| nc "+IP+" 1200")
                print("go")
            elif "back" in text:
                os.system("python3 ./commands/back.py | nc "+IP+" 1200")
                print("back")
            elif "stop" in text:
                os.system("python3 ./commands/stop.py | nc "+IP+" 1200")
                print("stop")
            elif "turn left" in text:
                os.system("python3 ./commands/left.py | nc "+IP+" 1200")
                print("left")
            elif "turn right" in text:
                os.system("python3 ./commands/right.py| nc "+IP+" 1200")
                print("right")

except KeyboardInterrupt:
    print("\nProgram terminated by user")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
