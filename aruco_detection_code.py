# code taken from: https://stackoverflow.com/questions/57392883/how-to-detect-aruco-markers-on-low-resolution-image
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import time
import numpy as np
import cv2
from cv2 import aruco

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

img = cv2.imread('image.png')

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)
parameters = aruco.DetectorParameters_create()

camera = PiCamera()
camera.resolution = (IMAGE_WIDTH,IMAGE_HEIGHT)

imageCapture = PiRGBArray(camera, size = camera.resolution)

camera.capture(imageCapture, format='bgr')
image = imageCapture.array

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Detect the markers.
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)
print(corners)
#if ids != 'None':
image = aruco.drawDetectedMarkers(image, corners, ids)

cv2.imwrite("aruco_detect.jpg", image)

#cv2.imshow("out",out)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
