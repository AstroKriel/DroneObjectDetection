from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import time
import numpy as np
import cv2

# set the amount of images to store
BUFFER_SIZE = 5
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

# declare image number count
num = 0

## load the opencv2 classifier models
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# initialise PiCamera and set resolution
camera = PiCamera()
camera.resolution = (IMAGE_WIDTH,IMAGE_HEIGHT)

# start loop to run until program terminated with Ctrl-C
try:
    while True:
        # capture image
        imageCapture = PiRGBArray(camera, size = (640,480))
        # format image
        camera.capture(imageCapture, format="bgr")
        image = imageCapture.array        
        # format the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        # identify any faces in the image
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # draw boxes around recognised faces
        for (x,y,w,h) in faces:
            image = cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            # draw boxes around recognised eyes
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        # write image to file
        cv2.imwrite("haar_" + str(num) + ".jpg", image)
        # increment file number and reset to zero if it exceeds buffer size
        num += 1
        if num == BUFFER_SIZE:
            num = 0
# exit program if Ctrl-C pressed
except KeyboardInterrupt:
    print("Press Ctrl-C to terminate")
    pass