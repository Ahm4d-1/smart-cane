from object_detector import * # to detect objects
from dist_sensor import *     # to find distance
from picamera.array import PiRGBArray # to get pi-camra array 
from picamera import PiCamera # to get pi-camera function
import time 
from threading import Thread 
from vibrator import *

dist = 0 # global initialization to avoid reference before assignment

# constants to meausre risk
upper_value = 100
lower_value = 30

# function to sense distance using ultrasonic sensor
def measure_distance():
    global dist
    while True:
        # store distance value in dist variable from dist_sensor.py file
        dist = distance()
        print ("Measured Distance = %.1f cm" % dist)
        time.sleep(1)
        
    
# function returns risk lvl on the user based on distance from object
def get_danger_lvl(dist):
    if dist > upper_value:
        return 'green'
    
    elif dist <= upper_value and dist > lower_value:
        return 'yellow'
    
    elif dist <= lower_value:
        return 'red'
    

# camera settings
camera = PiCamera()
camera.resolution = (1360, 768) # camera resolution
camera.framerate = 30 # camera framerate
rawCapture = PiRGBArray(camera, size=(1360, 768)) # start recording


# puting the senser function in a thread
sensor_thread = Thread(target=measure_distance, daemon=True)
sensor_thread.start()


# function in a seperate thread that handles vibration motor based on danger lvl
def start_vibration():
    while True:
        danger_lvl = get_danger_lvl(dist)
        if danger_lvl == 'red':
            vibrate(2, 30)
        elif danger_lvl == 'yellow':
            vibrate(1, 15)
        
# start thread for motor
motor_thread = Thread(target=start_vibration, daemon=True)
motor_thread.start()

# capture frames from the camera
try:
    global danger_lvl
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        result,objectInfo = getObjects(image,0.65,0.50,str(dist),objects=[])

        # show the frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        
except KeyboardInterrupt:
    print("Stopping Motor")
    # stop threads from running and kill them
    # clear GPIO using cleanup()
    sensor_thread.do_run = False
    motor_thread.do_run = False
    GPIO.cleanup()
    sensor_thread.join()
    motor_thread.join()
    
        



