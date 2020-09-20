from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import time
import requests
import numpy as np
import cv2
from cv2 import aruco
from threading import Thread

# Define resolution and framerate for captured video
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
FRAME_RATE = 5

# This is the url that image data will be posted to
imagesurl = "http://192.168.0.156:5000/images"

# Import the relevant ArUco marker dictionary
aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
parameters = aruco.DetectorParameters_create()


# Initialise camera
def init_Camera():
    global IMAGE_WIDTH, IMAGE_HEIGHT, FRAME_RATE

    # Initialise PiCamera
    camera = PiCamera()
    camera.resolution = (IMAGE_WIDTH, IMAGE_HEIGHT)
    camera.framerate = FRAME_RATE

    # Define video capture parameters
    rawCapture = PiRGBArray(camera, size = camera.resolution)

    # Allow the camera to warmup
    time.sleep(0.1)

    return camera, rawCapture


# Process image to detect any Aruco markers
def detect_Aruco(image):
    # Convert captured image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect the markers.
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

    # Markup the original image if marker detected
    if (len(corners) > 0):
        image = aruco.drawDetectedMarkers(image, corners, ids)
        ids = ids.flatten()

    return image, ids


# Process image to detect any A type targets
def detect_Targets(image):

    ##### Put Neco's target detection code #####

    # return updated image with detected target boxes #
    # return the  type of targets detected #
    detectedTargets = [None] * 2
    # if (A1 detected):
    #     detectedTargets[0] = True
    # if (A2 detected):
    #     detectedTargets[1] = True
    

    return image, detectedTargets


# Send current image to GCS
def send_Image(image, timestamp, detectedArucos, detectedTargets):
    global imagesurl
    # Set loop iterationstart time - Just for testing
    # start = time.time()

    # Save the image to file
    cv2.imwrite('current_image.jpg', image)

    # Create headers
    headers = {
        'imageTimestamp': str(timestamp.strftime('%Y-%m-%d_%H:%M:%S'))
    }
    
    if (detectedTargets[0] is not None):
        headers['A1-detected'] = 'True'
    if (detectedTargets[1] is not None):
        headers['A2-detected'] = 'True'
    if (detectedArucos is not None):
        headers['B-detected'] = str(detectedArucos)

    # Import image as file
    image_file = open('current_image.jpg', 'rb')
    files = {'current_image.jpg': image_file}
    # Post file to endpoint "http://192.168.0.156:5000/images"
    try:
        res = requests.post(imagesurl, files=files, headers=headers, timeout=4)
    except requests.Timeout:
        pass
    except requests.ConnectionError:
        pass

    image_file.close()

    # Print loop duration - Just for testing
    # print ('T2' + str(time.time() - start)) 



camera, rawCapture = init_Camera()

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Set loop iterationstart time - Just for testing
    # start = time.time()
    
    # Capture image using the PiCamera
    image = rawCapture.array
    timestamp = datetime.now()

    image, detectedArucos = detect_Aruco(image)
    image, detectedTargets = detect_Targets(image)

    # Create thread to save and post image
    Thread(target=send_Image, args=(image, timestamp, detectedArucos, detectedTargets)).start()

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # Print loop duration - Just for testing
    # print ('T1' + str(time.time() - start)) 
