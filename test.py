import sys
import cv2

print("Python version: \n" + sys.version)
print("cv2 version: " + cv2.__version__)

img = cv2.imread('smallRPi.JPG', cv2.IMREAD_UNCHANGED)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyWindow('image')
