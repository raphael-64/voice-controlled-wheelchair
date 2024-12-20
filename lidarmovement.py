import RPi.GPIO as GPIO
import time
from YDLidar import CYdLidar

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

# Initialize YDLIDAR
def init_lidar():
    lidar = CYdLidar()
    lidar.setlidaropt(CYdLidar.LidarPropSerialPort, "/dev/ttyUSB0")
    lidar.setlidaropt(CYdLidar.LidarPropSerialBaudrate, 128000)
    lidar.setlidaropt(CYdLidar.LidarPropLidarType, 0)
    lidar.setlidaropt(CYdLidar.LidarPropDeviceType, 0)
    lidar.setlidaropt(CYdLidar.LidarPropSampleRate, 5)
    lidar.setlidaropt(CYdLidar.LidarPropScanFrequency, 10)
    lidar.setlidaropt(CYdLidar.LidarPropSingleChannel, True)
    if lidar.initialize():
        print("YDLIDAR initialized.")
        return lidar
    else:
        print("Failed to initialize YDLIDAR.")
        return None

def get_lidar_data(lidar):
    scan = lidar.doProcessSimple(scan=None)
    if scan is not None:
        return {point.angle: point.range for point in scan.points}
    else:
        print("Failed to get lidar data.")
        return {}

try:
    lidar = init_lidar()
    if not lidar:
        raise Exception("LiDAR initialization failed")

    while True:
        # Get LiDAR data
        lidar_data = get_lidar_data(lidar)
        if not lidar_data:
            continue

        # Filter data
        front_distance = min([dist for angle, dist in lidar_data.items() if -10 <= angle <= 10], default=1000)
        left_distance = min([dist for angle, dist in lidar_data.items() if -90 <= angle < -30], default=1000)
        right_distance = min([dist for angle, dist in lidar_data.items() if 30 < angle <= 90], default=1000)

        # Decision-making based on LiDAR data
        if front_distance > 40:  # No obstacle ahead
            move_forward()
            time.sleep(2)
        else:  # Obstacle detected
            stop_motors()
            time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    if lidar:
        lidar.turnOff()
        lidar.disconnecting()
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    print("GPIO cleaned up.")
