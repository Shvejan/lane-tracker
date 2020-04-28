import cv2
import numpy as np

img = cv2.imread("road.jpg",0)
filter = cv2.Canny(img,50,150)

mask = np.zeros_like(img)

cv2.imshow("window",mask)
cv2.waitKey(0)
