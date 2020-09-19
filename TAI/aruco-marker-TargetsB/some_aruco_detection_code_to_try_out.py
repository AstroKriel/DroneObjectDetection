# code taken from: https://stackoverflow.com/questions/57392883/how-to-detect-aruco-markers-on-low-resolution-image

import cv2
from cv2 import aruco

img = cv2.imread('image.png')

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

# Detect the markers.
corners, ids, rejectedImgPoints = aruco.detectMarkers(img,aruco_dict,parameters=parameters)

out = aruco.drawDetectedMarkers(img, corners, ids)

cv2.imshow("out",out)
cv2.waitKey(0)
cv2.destroyAllWindows()