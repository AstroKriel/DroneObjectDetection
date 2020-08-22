import numpy as np
import cv2

## load the opencv2 classifier models
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

file_name = "cuties_2.png"
img_orig = cv2.imread(file_name)
gray = cv2.cvtColor(img_orig, cv2.COLOR_RGB2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)
img_detec = img_orig
for (x,y,w,h) in faces:
    img_detec = cv2.rectangle(img_detec,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img_detec[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

cv2.imwrite("haar_" + file_name, img_detec) 