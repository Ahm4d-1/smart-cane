import RPi.GPIO as GPIO
from time import sleep
 

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
# set GPIO pins values
motor_input1 = 17
motor_input2 = 27
motor_enable = 5


# setup GPIO for inputs
GPIO.setup(motor_input1,GPIO.OUT)
GPIO.setup(motor_input2,GPIO.OUT)
GPIO.setup(motor_enable,GPIO.OUT)
motor = GPIO.PWM(motor_enable, 1000)


# function for motor vibration
def vibrate(seconds, intensity):
    print("Turning motor on")
    GPIO.output(motor_input1,GPIO.HIGH)
    GPIO.output(motor_input2,GPIO.LOW)
     
    motor.start(intensity)
    sleep(seconds)

    print("Stopping motor")
    # To stop vibration
    GPIO.output(motor_input1,GPIO.LOW)
    GPIO.output(motor_input2,GPIO.LOW)
 

#vibrate(1, 30)
#GPIO.cleanup()