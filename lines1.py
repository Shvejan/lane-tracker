import cv2
import numpy as np




def coordinates(image,line_par):
    slope,inter = line_par
    y1=image.shape[0]
    y2=int((3/5)*y1)
    x1=int((y1-inter)/slope)
    x2 = int((y2-inter)/slope)
    return np.array([x1,y1,x2,y2])


def display(image, lines):
    blank = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            cv2.line(blank, (x1,y1),(x2,y2),(255,0,0),20)
        return blank
def avg (image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1,y1,x2,y2 = line.reshape(4)
        par = np.polyfit((x1,x2),(y1,y2), 1)
        slope = par[0]
        intercept = par[1]
        if slope <0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_avg = np.average(left_fit, axis=0)
    right_avg = np.average(right_fit, axis=0)
    left_line = coordinates(image,left_avg )
    right_line = coordinates(image,right_avg )
    return np.array([left_line,right_line])



original = cv2.imread("road.jpg")
img = np.copy(original)
img = cv2.cvtColor(original,cv2.COLOR_RGB2GRAY)

filter = cv2.Canny(img,50,150)



mask = np.zeros_like(img)
triangle = np.array([[(200,700),(1100,700), (550,250)]])
cv2.fillPoly(mask, triangle, 255)

merged = cv2.bitwise_and(filter, mask)
lines = cv2.HoughLinesP(merged, 2,np.pi/180,100 ,np.array([]),minLineLength=40,maxLineGap=5)
avg_lines = avg(original, lines)



line_img = display(img,avg_lines)
combined = cv2.addWeighted(img,0.8,line_img,1, 1)

cv2.imshow("window",combined)
cv2.waitKey(0)
