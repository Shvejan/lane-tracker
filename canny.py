import cv2


img = cv2.imread("road.jpg")
filter = cv2.Canny(img,50,150)



cv2.imshow("window",filter)
cv2.waitKey(0)
