from vosk import Model, KaldiRecognizer
import pyaudio
import socket
import threading
import subprocess
import os
import matplotlib.pyplot as plt
import numpy as np

# Voice recognition setup
model = Model("/Users/raphael/Documents/GitHub/voice-controlled-wheelchair/vosk-model")
recognizer = KaldiRecognizer(model, 16000)
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, input_device_index=0, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()

# Networking setup for LiDAR
LIDAR_IP = '192.168.137.38'  # Replace with Raspberry Pi's IP
LIDAR_PORT = 65433

# Visualization setup
plt.ion()
fig, ax = plt.subplots()
sc = ax.scatter([], [])
ax.set_xlim(-10, 10)  # Adjust as needed
ax.set_ylim(-10, 10)

# Command handling function
def handle_voice_commands():
    try:
        while True:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = eval(result)["text"]

                if "go" in text:
                    os.system(f"echo go | nc {LIDAR_IP} 1200")
                    print("go")
                elif "back" in text:
                    os.system(f"echo back | nc {LIDAR_IP} 1200")
                    print("back")
                elif "stop" in text:
                    os.system(f"echo stop | nc {LIDAR_IP} 1200")
                    print("stop")
                elif "turn left" in text:
                    os.system(f"echo turn left | nc {LIDAR_IP} 1200")
                    print("turn left")
                elif "turn right" in text:
                    os.system(f"echo turn right | nc {LIDAR_IP} 1200")
                    print("turn right")
                elif "slow down" in text:
                    os.system(f"echo slow down | nc {LIDAR_IP} 1200")
                    print("slow down")
                elif "speed up" in text:
                    os.system(f"echo speed up | nc {LIDAR_IP} 1200")
                    print("speed up")
                elif "destroy" in text:
                    os.system(f"echo destroy | nc {LIDAR_IP} 1200")
                    print("destroy")
    except KeyboardInterrupt:
        print("Voice command handling stopped.")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

# LiDAR data visualization function
def visualize_lidar():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((LIDAR_IP, LIDAR_PORT))
        print(f"Connected to LiDAR data at {LIDAR_IP}:{LIDAR_PORT}")

        try:
            while True:
                data = client.recv(1024).decode('utf-8').strip()
                if data:
                    print(f"LiDAR Data: {data}")
                    # Example: Parse "angle,distance" format to x, y
                    points = [tuple(map(float, p.split(','))) for p in data.split(';')]
                    x = [p[1] * np.cos(np.radians(p[0])) for p in points]
                    y = [p[1] * np.sin(np.radians(p[0])) for p in points]
                    sc.set_offsets(np.c_[x, y])
                    plt.draw()
                    plt.pause(0.01)
        except KeyboardInterrupt:
            print("LiDAR visualization stopped.")

# Run both voice commands and LiDAR visualization in parallel
if __name__ == "__main__":
    try:
        voice_thread = threading.Thread(target=handle_voice_commands)
        lidar_thread = threading.Thread(target=visualize_lidar)

        voice_thread.start()
        lidar_thread.start()

        voice_thread.join()
        lidar_thread.join()
    except KeyboardInterrupt:
        print("Program terminated.")
