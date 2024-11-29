import RPi.GPIO as GPIO
import time
import subprocess

TOUCH_SENSOR_PIN = 11
LED = 13

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

                file = open("output.txt", "w")  
                file.write("stop\n")
                file.close()  

                bash_process = subprocess.Popen(['bash', 'listener.sh'])
                python_process = subprocess.Popen(['python3', 'reader.py'])
                GPIO.output(LED, GPIO.HIGH)
                toggle_variable = 1
            else: 
                print("TERMINATING...")
                time.sleep(0.5)

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