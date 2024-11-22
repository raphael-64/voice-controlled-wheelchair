from vosk import Model, KaldiRecognizer
import pyaudio
import time

model = Model("/Users/steph/OneDrive/Documents/Coding/SE101/voice-controlled-wheelchair/vosk-model")  #just my laptop, add the right path 
recognizer = KaldiRecognizer(model, 16000)

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()


try:
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = eval(result)["text"]

            if "go" in text:
                print("go")
            elif "back" in text:
                print("back")
            elif "stop" in text:
                print("stop")
            elif "turn left" in text:
                print("left")
            elif "turn right" in text:
                print("right")
            elif "slow down" in text:
                print("down")
            elif "speed up" in text:
                print("up")
except KeyboardInterrupt:
    print("\nProgram terminated by user")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
