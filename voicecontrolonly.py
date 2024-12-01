from vosk import Model, KaldiRecognizer
import pyaudio
import socket
import threading
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

# LiDAR visualization logic
def visualize_lidar():
    plt.ion()
    fig, ax = plt.subplots()
    sc = ax.scatter([], [])
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            print(f"Connecting to LiDAR server at {LIDAR_IP}:{LIDAR_PORT}...")
            client.connect((LIDAR_IP, LIDAR_PORT))
            print(f"Connected to LiDAR server at {LIDAR_IP}:{LIDAR_PORT}")

            while True:
                data = client.recv(1024).decode('utf-8').strip()
                if data:
                    print(f"LiDAR Data: {data}")
                    points = [tuple(map(float, p.split(','))) for p in data.split(';')]
                    x = [p[1] * np.cos(np.radians(p[0])) for p in points]
                    y = [p[1] * np.sin(np.radians(p[0])) for p in points]
                    sc.set_offsets(np.c_[x, y])
                    plt.draw()
                    plt.pause(0.01)
    except ConnectionRefusedError:
        print(f"Error: Unable to connect to {LIDAR_IP}:{LIDAR_PORT}. Is the server running?")
    except Exception as e:
        print(f"Unexpected error in LiDAR visualization: {e}")
    finally:
        print("LiDAR visualization stopped.")

# Voice command handling
def handle_voice_commands():
    try:
        while True:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = eval(result)["text"]
                print(f"Voice Command: {text}")

                if "go" in text:
                    os.system(f"echo go | nc {LIDAR_IP} 1200")
                elif "back" in text:
                    os.system(f"echo back | nc {LIDAR_IP} 1200")
                elif "stop" in text:
                    os.system(f"echo stop | nc {LIDAR_IP} 1200")
                elif "turn left" in text:
                    os.system(f"echo turn left | nc {LIDAR_IP} 1200")
                elif "turn right" in text:
                    os.system(f"echo turn right | nc {LIDAR_IP} 1200")
                elif "slow down" in text:
                    os.system(f"echo slow down | nc {LIDAR_IP} 1200")
                elif "speed up" in text:
                    os.system(f"echo speed up | nc {LIDAR_IP} 1200")
                elif "destroy" in text:
                    os.system(f"echo destroy | nc {LIDAR_IP} 1200")
    except KeyboardInterrupt:
        print("Voice command handling stopped.")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    try:
        # Start the voice commands in a separate thread
        voice_thread = threading.Thread(target=handle_voice_commands, daemon=True)
        voice_thread.start()

        # Run the visualization in the main thread
        visualize_lidar()

    except KeyboardInterrupt:
        print("\nProgram terminated.")
