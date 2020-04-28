import cv2
import numpy as np
import matplotlib.pyplot as plt


def make_coor(image, line_par):
    slope1, intercepts = line_par
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1- intercepts)/slope1)
    x2 = int((y2- intercepts)/slope1)
    return np.array([x1,y1,x2,y2])



def avg_slop(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1,y1,x2,y2 = line.reshape(4)
        parametres = np.polyfit((x1,x2), (y1,y2), 1)
        slope = parametres[0]
        intercept = parametres[1]
        if (slope < 0):
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))

    left_avg = np.average(left_fit, axis=0)
    right_avg = np.average(right_fit, axis=0)

    left_line = make_coor(image, left_avg)
    right_line = make_coor(image, right_avg)
    return np.array([left_line, right_line])


def canny(image):
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny_image = cv2.Canny(blur, 50,150)
    return canny_image


def regionOfIntrest(image):
    height = image.shape[0]
    polygons = np.array([[(200,height), (1100,height), (550,250)]])
    mask =np.zeros_like(image)
    cv2.fillPoly(mask,polygons, 255)
    maskedImg = cv2.bitwise_and(image,mask)
    return maskedImg


def display(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            cv2.line(line_image, (x1,y1),(x2,y2), (255,0,255), 20)
    return line_image

cap = cv2.VideoCapture("t.mp4")







while(cap.isOpened()):
    _,frame = cap.read()

    canny_img = canny(frame)
    cropped = regionOfIntrest(canny_img)
    lines = cv2.HoughLinesP(cropped,2, np.pi/180, 100, np.array([]),minLineLength=40,maxLineGap=5 )
    avg_lines = avg_slop(frame, lines)
    line_img = display(frame, avg_lines)
    comboImg = cv2.addWeighted(frame, 0.4, line_img,0.6, 1)
    cv2.imshow('res',comboImg)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
