import RPi.GPIO as GPIO
import time
import random

# Motor Pins Setup
PIN1_A = 29  # In1 A
PIN2_A = 31  # In2 A
ENA_A = 33   # PWM motor A

PIN1_B = 40  # In3 for Motor B
PIN2_B = 38  # In4 for Motor B
ENA_B = 32   # PWM for Motor B

GPIO.setmode(GPIO.BOARD)

# Setup Motor A pins
GPIO.setup(PIN1_A, GPIO.OUT)
GPIO.setup(PIN2_A, GPIO.OUT)
GPIO.setup(ENA_A, GPIO.OUT)

# Setup Motor B pins
GPIO.setup(PIN1_B, GPIO.OUT)
GPIO.setup(PIN2_B, GPIO.OUT)
GPIO.setup(ENA_B, GPIO.OUT)

# Initialize PWM
pwm_a = GPIO.PWM(ENA_A, 100)
pwm_b = GPIO.PWM(ENA_B, 100)
pwm_a.start(50)
pwm_b.start(50)

# Movement functions
def move_forward():
    GPIO.output(PIN1_A, GPIO.HIGH)
    GPIO.output(PIN2_A, GPIO.LOW)
    GPIO.output(PIN1_B, GPIO.LOW)
    GPIO.output(PIN2_B, GPIO.HIGH)
    print("Moving forward")

def move_backward():
    GPIO.output(PIN1_A, GPIO.LOW)
    GPIO.output(PIN2_A, GPIO.HIGH)
    GPIO.output(PIN1_B, GPIO.HIGH)
    GPIO.output(PIN2_B, GPIO.LOW)
    print("Moving backward")

def turn_right_intermediate():
    GPIO.output(PIN1_A, GPIO.LOW)
    GPIO.output(PIN2_A, GPIO.HIGH)
    GPIO.output(PIN1_B, GPIO.HIGH)
    GPIO.output(PIN2_B, GPIO.LOW)
    print("Turning slightly right")

def turn_left_intermediate():
    GPIO.output(PIN1_A, GPIO.HIGH)
    GPIO.output(PIN2_A, GPIO.LOW)
    GPIO.output(PIN1_B, GPIO.LOW)
    GPIO.output(PIN2_B, GPIO.HIGH)
    print("Turning slightly left")

def stop_motors():
    GPIO.output(PIN1_A, GPIO.LOW)
    GPIO.output(PIN2_A, GPIO.LOW)
    GPIO.output(PIN1_B, GPIO.LOW)
    GPIO.output(PIN2_B, GPIO.LOW)
    print("Stopping")

# Simulated LiDAR data generation
def simulate_lidar_data():
    """
    Generate a pseudo-random set of distances in a 180-degree arc.
    Returns a dictionary with angles as keys and distances as values.
    """
    lidar_data = {}
    for angle in range(-90, 91, 10):  # -90° to 90° in 10° steps
        lidar_data[angle] = random.randint(20, 100)  # Random distance between 20 and 100 cm
    return lidar_data

try:
    while True:
        # Simulate LiDAR data
        lidar_data = simulate_lidar_data()
        print(f"Simulated LiDAR Data: {lidar_data}")

        # Decision-making based on LiDAR data
        front_distance = lidar_data[0]  # Distance directly ahead
        left_distance = min(lidar_data[angle] for angle in range(-90, -30, 10))  # Check left angles
        right_distance = min(lidar_data[angle] for angle in range(30, 91, 10))   # Check right angles

        if front_distance > 40:  # No obstacle ahead
            move_forward()
            time.sleep(2)
        else:  # Obstacle detected
            stop_motors()
            time.sleep(1)

            if left_distance > right_distance:
                print("Obstacle ahead! Turning slightly left.")
                for _ in range(3):  # Perform intermediate left turns
                    turn_left_intermediate()
                    time.sleep(0.5)
                    move_forward()
                    time.sleep(0.5)
            else:
                print("Obstacle ahead! Turning slightly right.")
                for _ in range(3):  # Perform intermediate right turns
                    turn_right_intermediate()
                    time.sleep(0.5)
                    move_forward()
                    time.sleep(0.5)

            stop_motors()
            print("Reevaluating path...")
            time.sleep(1)

except KeyboardInterrupt:
    print("Simulation interrupted by user.")

finally:
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    print("GPIO cleaned up.")
