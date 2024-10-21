import os
import cv2 as cv 
import numpy as np

# SHOW PHOTO
img_path = 'photo/pato.jpg'

img = cv.imread(img_path)

if img is None:
    print("Error: Could not load image.")
else:
    cv.imshow('Jhonta', img)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    threshold, thresh = cv.threshold(gray, 120, 255, cv.THRESH_BINARY )
    cv.imshow('simple thresh', thresh)
    
    adaptThresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 5)
    cv.imshow("adapt or die", adaptThresh)
    
    cv.waitKey(0)
    