import RPi.GPIO as GPIO
import time

TOUCH_SENSOR_PIN = 11
toggle_variable = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#print("Press the touch sensor to toggle the variable.")

try:
    while True:
        if GPIO.input(TOUCH_SENSOR_PIN) == GPIO.LOW:  
            toggle_variable = 1 - toggle_variable
            #print(f"Variable is now: {toggle_variable}")
            time.sleep(0.5)  
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()