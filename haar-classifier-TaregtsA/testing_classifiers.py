import cv2
import numpy as np
import matplotlib.pyplot as plt

## load cascade classifiers
target_A1_cascade = cv2.CascadeClassifier('cascadeA1.xml')
target_A2_cascade = cv2.CascadeClassifier('cascadeA2.xml')

## load image
file_name = "TargetA2.png"
img_orig = cv2.imread(file_name)
gray = cv2.cvtColor(img_orig, cv2.COLOR_RGB2GRAY)

## classify targets
targets = target_A2_cascade.detectMultiScale(gray)
for (x, y, w, h) in targets:
    cv2.rectangle(img_orig, (x, y), (x+w, y+h), (255, 0, 0), 2)

plt.imshow(img_orig)
plt.show()

