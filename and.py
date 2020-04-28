import cv2
import numpy as np

img = cv2.imread("road.jpg",0)
filter = cv2.Canny(img,50,150)

mask = np.zeros_like(img)
triangle = np.array([[(200,700),(1100,700), (550,250)]])
cv2.fillPoly(mask, triangle, 255)

merged = cv2.bitwise_and(filter, mask)

cv2.imshow("window",merged)
cv2.waitKey(0)
