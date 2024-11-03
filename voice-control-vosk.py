from vosk import Model, KaldiRecognizer
import pyaudio

model = Model("/Users/raphael/Documents/Github/voice-controlled-wheelchair/vosk-model")  #just my laptop, add the right path 
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
                # activate GPIO for forward motion
                print("Command: Go")
            elif "stop" in text:
                # GPIO for stop
                print("Command: Stop")
            elif "turn left" in text:
                print("Command: Turn Left")
            elif "turn right" in text:
                print("Command: Turn Right")
            elif "slow down" in text:
                print("Command: Slow Down")
            elif "speed up" in text:
                print("Command: Speed Up")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
