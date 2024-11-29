import RPi.GPIO as GPIO
import time
import subprocess

TOUCH_SENSOR_PIN = 11
LED = 13

# Left
PIN1_A = 29 #In1 A
PIN2_A = 31 #in2 A
ENA_A = 33 #PWM motor

# Right
PIN1_B = 40   # IN3 for Motor B
PIN2_B = 38   # IN4 for Motor B
ENA_B = 32   # PWM for Motor B

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


toggle_variable = 0

GPIO.setmode(GPIO.BOARD)  # Use Broadcom pin-numbering scheme
GPIO.setup(TOUCH_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED, GPIO.OUT)


try:
    while True:
        if GPIO.input(TOUCH_SENSOR_PIN) == GPIO.HIGH:  
            # print("HELLO")
            # toggle_variable = 1 - toggle_variable
            if toggle_variable == 0:
                print("INITIATING...")
                time.sleep(0.5)

                # file = open("output.txt", "w")  
                # file.write("stop\n")
                # file.close()  

                bash_process = subprocess.Popen(['bash', 'listener.sh'])
                python_process = subprocess.Popen(['python3', 'reader.py'])
                GPIO.output(LED, GPIO.HIGH)
                toggle_variable = 1
            else: 
                print("TERMINATING...")
                time.sleep(0.5)

                GPIO.output(PIN1_A, GPIO.LOW)
                GPIO.output(PIN2_A, GPIO.LOW)
                    
                GPIO.output(PIN1_B, GPIO.LOW)
                GPIO.output(PIN2_B, GPIO.LOW)

                file = open("output.txt", "w")  
                file.write("stop\n")
                file.close() 

                bash_process.terminate()
                python_process.terminate()
                GPIO.output(LED, GPIO.LOW)
                toggle_variable = 0

            time.sleep(0.5)  
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()