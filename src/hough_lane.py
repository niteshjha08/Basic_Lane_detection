import cv2
import numpy as np
import math

def nothing(x):
    a=2
image=cv2.imread('lanes.PNG')
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

canny=cv2.Canny(gray,100,200)
canny_3d=np.dstack((canny,canny,canny))

# rho=1

cv2.namedWindow('frame')
cv2.createTrackbar('rho','frame',1,20,nothing)
cv2.createTrackbar('theta','frame',1,180,nothing)
cv2.createTrackbar('threshold','frame',1,20,nothing)
cv2.createTrackbar('min_line_length','frame',1,100,nothing)
cv2.createTrackbar('max_line_gap','frame',1,50,nothing)
shape=gray.shape
print(shape)
points=np.array([[(0,shape[0]),(int(shape[1]/3),int(shape[0]/2)),(2*int(shape[1]/3),int(shape[0]/2)),(shape[1],shape[0])]],dtype=np.int32)
mask=canny.copy()*0
cv2.fillPoly(mask,points,255)



cv2.imshow('imgae',image)
cv2.imshow('mask',mask)
while(cv2.waitKey(1)!=ord('q')):
    roi_image = cv2.bitwise_and(canny, mask)
    frame=canny_3d.copy()
    rho = cv2.getTrackbarPos('rho', 'frame')
    theta = cv2.getTrackbarPos('theta', 'frame')
    threshold = cv2.getTrackbarPos('threshold', 'frame')
    min_line_length = cv2.getTrackbarPos('min_line_length', 'frame')
    max_line_gap = cv2.getTrackbarPos('max_line_gap', 'frame')
    try:
        lines = cv2.HoughLinesP(roi_image, rho, theta*math.pi/180, threshold, np.array([]),min_line_length, max_line_gap)
    except:
        pass
    for line in lines:
        cv2.line(frame, (line[0, 0], line[0, 1]), (line[0, 2], line[0, 3]), (0, 0, 255), 2)
    cv2.imshow('frame',frame)




