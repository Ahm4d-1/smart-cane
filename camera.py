from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (1920, 1080)
camera.framerate = 30
camera.start_preview(alpha=200)
sleep(5)
camera.capture('/home/pi/Desktop/max.jpg')
camera.stop_preview()