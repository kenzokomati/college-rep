import os
import cv2 as cv  # type: ignore

img_path = 'C:/Users/user/OneDrive/Documentos/GitHub/College/Machine Learning/openCV/photo/jhonta.png'
if not os.path.exists(img_path):
    print("Error: File does not exist.")
else:
    img = cv.imread(img_path)
    if img is None:
        print("Error: Could not load image.")
    else:
        cv.imshow('Jhonta', img)
        cv.waitKey(0)
        cv.destroyAllWindows()
