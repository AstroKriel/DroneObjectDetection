#!/usr/bin/env python3
import time
import colorsys
import sys
import ST7735
import json
import requests
import pyaudio
import numpy as np
import math
import cv2

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
from enviroplus import gas
from enviroplus.noise import Noise
from subprocess import PIPE, Popen
from fonts.ttf import RobotoMedium as UserFont
from threading import Thread, Event
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
from cv2 import aruco

# Define resolution and framerate for captured video
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
FRAME_RATE = 5

# Import the relevant ArUco marker dictionary
aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
parameters = aruco.DetectorParameters_create()

# BME280 temperature/pressure/humidity sensor
bme280 = BME280()

# MEMS microphone
noise = Noise()

# initialise audio
audio = pyaudio.PyAudio()

# This is the url that sensor data will be posted to
sensorsurl = "http://192.168.0.156:5000/sensordata"
# This is the url that image data will be posted to
imagesurl = "http://192.168.0.156:5000/images"

#Full-scale dB range of microphone
WAIT_TIME = 10

stop_threads = False

# function to convert from PCM to dbSPL
def PCM_to_dbSPL(pcm):
    FSdbSPL = 120
    res = 0.0
    if pcm > 0:
        dbFS = 20 * math.log10(pcm / 0x1ffff)
        res = FSdbSPL + dbFS
    return res

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

cpu_temps = [get_cpu_temperature()] * 5

def retrieve_temp():
    global cpu_temps, bme280

    # Tuning factor for compensation. Decrease this number to adjust the
    # temperature down, and increase to adjust up
    factor = 0.85

    unit = "C"
    cpu_temp = get_cpu_temperature()
    # Smooth out with some averaging to decrease jitter
    cpu_temps = cpu_temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
    raw_temp = bme280.get_temperature()
    data = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
    return data, unit

def retrieve_pressure():
    global bme280

    unit = "hPa"
    data = bme280.get_pressure()
    return data, unit

def retrieve_humidity():
    global bme280

    unit = "%"
    data = bme280.get_humidity()
    return data, unit

def retrieve_lux():
    unit = "Lux"
    data = ltr559.get_lux()
    return data, unit

def retrieve_noise():
    global noise

    unit = "dB"
    low, mid, high, amp = noise.get_noise_profile()
    return amp, unit

def retrieve_gas():
    data = gas.read_all()

    # oxidising
    oxidising_unit = "kohm"
    oxidising = data.oxidising / 1000 # conversion from Ohms to kOhms
    data_oxidising = {"data": oxidising, "unit": oxidising_unit}

    # reducing
    reducing_unit = "kohm"
    reducing = data.reducing / 1000
    data_reducing = {"data": reducing, "unit": reducing_unit}

    # nh3
    nh3_unit = "kohm"
    nh3 = data.nh3 / 1000
    data_nh3 = {"data": nh3, "unit": nh3_unit}

    return data_oxidising, data_reducing, data_nh3


# The main loop
def other_sensors(e):
    global WAIT_TIME, stop_threads

    WAIT_TIME_SECONDS = 1
    CalibrateTime = 120
    mode = 0
    counter = 0
    ticker = Event()
    while not stop_threads:
        if not ticker.wait(WAIT_TIME_SECONDS):
            if mode == 0:
                counter = counter + 1
                baseline_oxidising, baseline_reducing, baseline_nh3 = retrieve_gas()
                data = {
                    "msg" : "%s seconds of calibration left" % (CalibrateTime-counter)
                }
                if counter == CalibrateTime:
                    baseline_data_oxidising = baseline_oxidising["data"]
                    baseline_data_reducing = baseline_reducing["data"]
                    baseline_data_nh3 = baseline_nh3["data"]
                    mode = 1
                elif counter == CalibrateTime-WAIT_TIME:
                    #trigger noise sensor thread to resume
                    e.set()

            elif mode == 1:
                temp, temp_unit = retrieve_temp()
                pressure, pressure_unit = retrieve_pressure()
                humidity, humidity_unit = retrieve_humidity()
                lux, lux_unit = retrieve_lux()
                data_oxidising, data_reducing, data_nh3 = retrieve_gas()

                oxidising_val = ((data_oxidising["data"] - baseline_data_oxidising) / baseline_data_oxidising)*100
                reducing_val = -((data_reducing["data"] - baseline_data_reducing) / baseline_data_reducing)*100
                nh3_val = -((data_nh3["data"] - baseline_data_nh3) / baseline_data_nh3)*100

                data = {
                    "temperature" : {"data": temp, "unit": temp_unit},
                    "pressure": {"data": pressure, "unit": pressure_unit},
                    "humidity": {"data": humidity, "unit": humidity_unit},
                    "lux": {"data": lux, "unit": lux_unit},
                    "gas" : {"oxidising":{"data": oxidising_val, "unit": "%"},
                             "reducing":{"data": reducing_val, "unit": "%"},
                             "nh3":{"data": nh3_val, "unit": "%"}}
                }
            print(data)
            try:
                r = requests.post(sensorsurl, json=data, timeout=0.01)
            except requests.Timeout:
                # back off and retry
                pass
            except requests.ConnectionError:
                pass




def noise_sensor(e):
    global WAIT_TIME, stop_threads

    if not e.isSet():
        e.wait()

    RATE = 22000
    CHUNK = 11000
    CHANNEL = 1

    stream = audio.open(format=pyaudio.paInt32,
                        input_device_index=2,
                        channels=CHANNEL,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    MSec = 0
    Sum = 0.0
    Cnt = 0
    noisefloor = 1e12
    maxSPL = 0.0
    while not stop_threads:
        if MSec >= 1000*WAIT_TIME:
            sdata = stream.read(CHUNK)
            idata = np.frombuffer(bytes(sdata), '<i4')
            fdata = idata.astype(float)
            vmax = (np.amax(fdata)) / 0x4000
            vmin = (np.amin(fdata)) / 0x4000
            DCoffset = (np.sum(fdata)) / (0x4000 * fdata.size)
            vmax_nodc = vmax - DCoffset
            vmin_nodc = vmin - DCoffset
            if abs(vmax_nodc) > abs(vmin_nodc):
                vabs = abs(vmax_nodc)
            else:
                vabs = abs(vmin_nodc)

            if vabs < noisefloor:
                noisefloor = vabs

            vfinal = vabs - noisefloor

            dbSPL = PCM_to_dbSPL(vfinal)
            if dbSPL > maxSPL:
                maxSPL = dbSPL

            data = {
                "noise": {"data": dbSPL, "unit": "dbSPL"}
            }
            print(data)

            try:
                r = requests.post(sensorsurl, json=data, timeout=0.01)
            except requests.Timeout:
                # back off and retry
                pass
            except requests.ConnectionError:
                pass


        else:
            sdata = stream.read(CHUNK)
            MSec = MSec + 500


    stream.stop_stream()
    stream.close()
    audio.terminate()




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


def image_processing(e):
    global stop_threads

    # Setup PiCamera
    camera, rawCapture = init_Camera()

    # Keep the main thread running, otherwise signals are ignored.
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # # Set loop iterationstart time - Just for testing
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

        # Break loop if threads stopped
        if (stop_threads):
            break

        # # Print loop duration - Just for testing
        # print ('T1' + str(time.time() - start)) 


if __name__ == '__main__':
    try:
        # event to synchronise threads to ensure they start at the same time
        e = Event()
        t1 = Thread(target=other_sensors, args=(e,))
        t2 = Thread(target=noise_sensor, args=(e,))
        t3 = Thread(target=image_processing, args=(e,))
        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
        # starting thread 3
        t3.start()

        # main loop
        while (True):
            time.sleep(1)


    except KeyboardInterrupt:
        print('Closing threads...')
        stop_threads = True
        # if program closed before thread 1 flags calibration is done, ensure thread 2 is unblocked and hence able to run to completion
        if not e.isSet():
            e.set()
        # Wait for the threads to close
        t1.join()
        # starting thread 2
        t2.join()