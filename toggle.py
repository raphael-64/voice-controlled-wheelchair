import RPi.GPIO as GPIO
import time
import subprocess

TOUCH_SENSOR_PIN = 11
toggle_variable = 0

GPIO.setmode(GPIO.BOARD)  # Use Broadcom pin-numbering scheme
GPIO.setup(TOUCH_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

bash_process = None
python_process = None

try:
    while True:
        if GPIO.input(TOUCH_SENSOR_PIN) == GPIO.HIGH:  
            # print("HELLO")
            # toggle_variable = 1 - toggle_variable
            if toggle_variable == 0:
                print("INITIATING...")
                time.sleep(0.5)
                bash_process = subprocess.Popen(['bash', 'listener.sh'])
                python_process = subprocess.Popen(['python3', 'reader.py'])
                toggle_variable = 1
            else: 
                print("TERMINATING...")
                time.sleep(0.5)
                if bash_process:
                    bash_process.terminate()
                    bash_process.wait()
                if python_process:
                    python_process.terminate()
                    python_process.wait()
                toggle_variable = 0

            time.sleep(0.5)  
except KeyboardInterrupt:
    print("Exiting...")
finally:
    if bash_process:
        bash_process.terminate()
        bash_process.wait()
    if python_process:
        python_process.terminate()
        python_process.wait()
    GPIO.cleanup()