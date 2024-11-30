import os
import RPi.GPIO as GPIO
import time
import threading  # For running motor control and LiDAR simultaneously
import socket  # For sending LiDAR data
import serial  # For LiDAR communication

# --- Motor Control Setup ---
# Left
PIN1_A = 29  # In1 A
PIN2_A = 31  # In2 A
ENA_A = 33  # PWM motor

# Right
PIN1_B = 40  # IN3 for Motor B
PIN2_B = 38  # IN4 for Motor B
ENA_B = 32  # PWM for Motor B

GPIO.setmode(GPIO.BOARD)  # Use Broadcom pin-numbering scheme

# Setup Motor A pins
GPIO.setup(PIN1_A, GPIO.OUT)
GPIO.setup(PIN2_A, GPIO.OUT)
GPIO.setup(ENA_A, GPIO.OUT)

# Setup Motor B pins
GPIO.setup(PIN1_B, GPIO.OUT)
GPIO.setup(PIN2_B, GPIO.OUT)
GPIO.setup(ENA_B, GPIO.OUT)

# Initialize PWM on ENA and ENB pins at 100Hz
pwm_a = GPIO.PWM(ENA_A, 100)  # Motor A PWM
pwm_b = GPIO.PWM(ENA_B, 100)  # Motor B PWM
pwm_a.start(50)
pwm_b.start(50)

# --- LiDAR Setup ---
LIDAR_PORT = '/dev/ttyUSB0'  # Update based on your LiDAR device
LIDAR_BAUDRATE = 115200

try:
    lidar = serial.Serial(LIDAR_PORT, baudrate=LIDAR_BAUDRATE, timeout=1)
except Exception as e:
    print(f"Failed to connect to LiDAR: {e}")
    lidar = None

# --- Networking Setup ---
LIDAR_HOST = "0.0.0.0"  # Listen on all interfaces
LIDAR_PORT = 65433  # Port to send LiDAR data

# --- Function to Handle Motor Control ---
def motor_control():
    try:
        while True:
            input = open("output.txt").read().strip()
            print("Input: " + input)
            if input == "left":
                GPIO.output(PIN1_A, GPIO.HIGH)
                GPIO.output(PIN2_A, GPIO.LOW)
                GPIO.output(PIN1_B, GPIO.HIGH)
                GPIO.output(PIN2_B, GPIO.LOW)

            elif input == "right":
                GPIO.output(PIN1_A, GPIO.LOW)
                GPIO.output(PIN2_A, GPIO.HIGH)
                GPIO.output(PIN1_B, GPIO.LOW)
                GPIO.output(PIN2_B, GPIO.HIGH)

            elif input == "back":
                GPIO.output(PIN1_A, GPIO.LOW)
                GPIO.output(PIN2_A, GPIO.HIGH)
                GPIO.output(PIN1_B, GPIO.HIGH)
                GPIO.output(PIN2_B, GPIO.LOW)
                time.sleep(2)

            elif input == "go":
                GPIO.output(PIN1_A, GPIO.HIGH)
                GPIO.output(PIN2_A, GPIO.LOW)
                GPIO.output(PIN1_B, GPIO.LOW)
                GPIO.output(PIN2_B, GPIO.HIGH)
                time.sleep(2)

            elif input == "stop":
                GPIO.output(PIN1_A, GPIO.LOW)
                GPIO.output(PIN2_A, GPIO.LOW)
                GPIO.output(PIN1_B, GPIO.LOW)
                GPIO.output(PIN2_B, GPIO.LOW)

            elif input == "destroy":
                GPIO.output(PIN1_A, GPIO.LOW)
                GPIO.output(PIN2_A, GPIO.LOW)
                GPIO.output(PIN1_B, GPIO.LOW)
                GPIO.output(PIN2_B, GPIO.LOW)
                pwm_a.ChangeDutyCycle(0)
                pwm_b.ChangeDutyCycle(0)
                pwm_a.stop()
                pwm_b.stop()
                GPIO.cleanup()
                break

    except KeyboardInterrupt:
        print("Motor control interrupted")
        GPIO.cleanup()

# --- Function to Send LiDAR Data ---
def send_lidar_data():
    if not lidar:
        print("LiDAR is not connected. Skipping LiDAR data transmission.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((LIDAR_HOST, LIDAR_PORT))
        server.listen(1)
        print(f"LiDAR server listening on {LIDAR_HOST}:{LIDAR_PORT}")
        conn, addr = server.accept()
        print(f"Connected by {addr} for LiDAR data")

        try:
            while True:
                if lidar.in_waiting > 0:
                    # Read LiDAR data
                    lidar_data = lidar.readline().decode('utf-8').strip()
                    print(f"LiDAR Data: {lidar_data}")

                    # Send data to the connected client
                    conn.sendall((lidar_data + '\n').encode('utf-8'))

        except KeyboardInterrupt:
            print("LiDAR data transmission interrupted")
        finally:
            conn.close()

# --- Main Program ---
if __name__ == "__main__":
    try:
        # Run motor control and LiDAR transmission in parallel
        motor_thread = threading.Thread(target=motor_control)
        lidar_thread = threading.Thread(target=send_lidar_data)

        motor_thread.start()
        lidar_thread.start()

        motor_thread.join()
        lidar_thread.join()

    except KeyboardInterrupt:
        print("Program interrupted by user")
        GPIO.cleanup()
        if lidar:
            lidar.close()
