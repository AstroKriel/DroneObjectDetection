from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import time
import numpy as np
import cv2
from cv2 import aruco

# Define resolution and framerate for captured video
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

# Import the relevant ArUco marker dictionary
aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
parameters = aruco.DetectorParameters_create()

# Initialise PiCamera
camera = PiCamera()
camera.resolution = (IMAGE_WIDTH, IMAGE_HEIGHT)
camera.framerate = 5

# Define video capture parameters
rawCapture = PiRGBArray(camera, size = camera.resolution)

# Allow the camera to warmup
time.sleep(0.1)

count = 0

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    start = time.time()
    
    # Capture image using the PiCamera
    image = rawCapture.array

    # Convert captured image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect the markers.
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

    # Log the number of ArUco markers detected
    if (len(corners) > 0):
        print(len(corners))

    # Draw marker detection onto the original image
    image = aruco.drawDetectedMarkers(image, corners, ids)

    # Save the image to file
    cv2.imwrite("aruco_detect_" + str(count) + ".jpg", image)
    count = count + 1
    	
    # Print loop duration
    print (str(time.time() - start))

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
