# code taken from: https://stackoverflow.com/questions/57392883/how-to-detect-aruco-markers-on-low-resolution-image
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import time
import numpy as np
import cv2
from cv2 import aruco

# Define resolution for captured images
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

# Import the relevant ArUco marker dictionary
aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
parameters = aruco.DetectorParameters_create()

# Initialise PiCamera
camera = PiCamera()
camera.resolution = (IMAGE_WIDTH,IMAGE_HEIGHT)

# Define image capture parameters
imageCapture = PiRGBArray(camera, size = camera.resolution)

# Capture image using the PiCamera
camera.capture(imageCapture, format='bgr')
image = imageCapture.array

# Convert captured image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect the markers.
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

# Log the number of ArUco markers detected
print(len(corners))

# Draw marker detection onto the original image
image = aruco.drawDetectedMarkers(image, corners, ids)

# Save the image to file
cv2.imwrite("aruco_detect.jpg", image)
