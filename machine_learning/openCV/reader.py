import os
import cv2 as cv 
import numpy as np


def rescaleFrame(frame, scale=0.75):
    height = int(frame.shape[0] * scale)
    width = int(frame.shape[1] * scale)
    dimensions = (width, height)
    
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


# SHOW PHOTO
img_path = 'photo/pato.jpg'

img = cv.imread(img_path)

if img is None:
    print("Error: Could not load image.")
else:
    cv.imshow('Jhonta', img)
    
    blank = np.zeros(img.shape, dtype='uint8')
    # cv.imshow('Blank', blank)
    
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv.imshow('Gray', gray)
    
    # blur = cv.GaussianBlur(gray, (5,5), cv.BORDER_DEFAULT)
    # cv.imshow('Blur', blur)
    
    canny = cv.Canny(gray, 125, 175)
    cv.imshow('Edges', canny)
    
    ret, thresh = cv.threshold(gray, 125, 225, cv.THRESH_BINARY)
    cv.imshow('Thresh', thresh)
    
    contours, hierarchies = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    
    print(f'{len(contours)} contours found')
    
    cv.drawContours(blank, contours, -1, (0,255,0), 1)
    cv.imshow('Contours drawn', blank)
    
    cv.waitKey(0)


## SHOW VIDEO
# capture = cv.VideoCapture('video\karina.mp4')

# while True:
#     isTrue, frame = capture.read()
    
#     frameResized = rescaleFrame(frame)
    
#     cv.imshow('Video', frame)
#     cv.imshow('Video Resized', frameResized)
    
    
#     if cv.waitKey(20) & 0xFF==ord('d'):
#         break
    
# capture.release()
# cv.destroyAllWindows()