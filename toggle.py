import RPi.GPIO as GPIO
import time
import subprocess

TOUCH_SENSOR_PIN = 11
toggle_variable = 0

GPIO.setmode(GPIO.BOARD)  # Use Broadcom pin-numbering scheme
GPIO.setup(TOUCH_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#print("Press the touch sensor to toggle the variable.")

try:
    while True:
        if GPIO.input(TOUCH_SENSOR_PIN) == GPIO.LOW:  
            toggle_variable = 1 - toggle_variable
            if toggle_variable == 0:
                print("NOT RUNNING")
                toggle_variable = 1
            else: 
                print("RUNNING")
                toggle_variable = 0

            time.sleep(0.5)  
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()