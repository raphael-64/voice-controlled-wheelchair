import pigpio
import time

pi = pigpio.pi()
# Left
PIN1_A = 29 #In1 A
PIN2_A = 31 #in2 A
ENA_A = 33 #PWM motor

# Right
PIN1_B = 40   # IN3 for Motor B
PIN2_B = 38   # IN4 for Motor B
ENA_B = 32   # PWM for Motor B


# Setup Motor A pins
pi.set_mode(PIN1_A, pigpio.OUTPUT)
pi.set_mode(PIN2_A, pigpio.OUTPUT)
pi.set_mode(ENA_A, pigpio.OUTPUT)
pi.set_mode(PIN1_B, pigpio.OUTPUT)
pi.set_mode(PIN2_B, pigpio.OUTPUT)
pi.set_mode(ENA_B, pigpio.OUTPUT)


pi.set_PWM_frequency(ENA_A, 100)  # 100 Hz frequency for Motor A
pi.set_PWM_dutycycle(ENA_A, 255)  # Full speed
pi.set_PWM_frequency(ENA_B, 100)  # 100 Hz frequency for Motor B
pi.set_PWM_dutycycle(ENA_B, 255)  # Full speed

input = open("output.txt").read()
print("Input:" + input)
        
if input == "go\n":    
    pi.write(PIN1_A, 1)
    pi.write(PIN2_A, 0)
    pi.write(PIN1_B, 1)
    pi.write(PIN2_B, 0)
    print("g")
elif input == "back\n":
    pi.write(PIN1_A, 0)
    pi.write(PIN2_A, 1)
    pi.write(PIN1_B, 0)
    pi.write(PIN2_B, 1)

elif input == "left\n": 
    pi.write(PIN1_A, 0)
    pi.write(PIN2_A, 1)
    pi.write(PIN1_B, 1)
    pi.write(PIN2_B, 0)

elif input == "right\n":
    pi.write(PIN1_A, 1)
    pi.write(PIN2_A, 0)
    pi.write(PIN1_B, 0)
    pi.write(PIN2_B, 1)
elif input == "stop\n":
    pi.write(PIN1_A, 0)
    pi.write(PIN2_A, 0)
    pi.write(PIN1_B, 0)
    pi.write(PIN2_B, 0)
    pi.set_PWM_dutycycle(ENA_A, 0)  # Stop Motor A
    pi.set_PWM_dutycycle(ENA_B, 0)  # Stop Motor B 
    pi.set_PWM_dutycycle(ENA_A, 0)
    pi.set_PWM_dutycycle(ENA_B, 0)
    pi.stop()  # Disconnect from pigpio daemon
