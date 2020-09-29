import cv2
import numpy as np
import math

image=cv2.imread('test_images/solidWhiteCurve.jpg')
img=image.copy()
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# COLOR THRESHOLDING
red_thresh=200
green_thresh=200
blue_thresh=200
rgb_thresh=[blue_thresh,green_thresh,red_thresh]

color_threshold=(img[:,:,0]<rgb_thresh[0]) | (img[:,:,1]<rgb_thresh[1]) | (img[:,:,2]<rgb_thresh[2])

img[color_threshold]=[0,0,0]
gray[color_threshold]=0
canny=cv2.Canny(gray,50,150)

# REGION MASKING
shape=img.shape

right_coordinates=np.array([[(480,shape[0]),(480,320),(640,320),(shape[1],shape[0])]],dtype=np.int32)
left_coordinates=np.array([[(0,shape[0]),(320,320),(480,320),(480,shape[0])]],dtype=np.int32)
blackl=gray.copy()*0
blackr=blackl.copy()
left_mask=cv2.fillPoly(blackl,left_coordinates,255)
right_mask=cv2.fillPoly(blackr,right_coordinates,255)

# FITTING SLOPES OF LEFT AND RIGHT LINES
roi_left=cv2.bitwise_and(canny,left_mask)
roi_right=cv2.bitwise_and(canny,right_mask)
left_lines=cv2.HoughLinesP(roi_left,2,math.pi/180,5,np.array([]),20,50)
right_lines=cv2.HoughLinesP(roi_right,2,math.pi/180,5,np.array([]),20,50)

xs=list()
ys=list()
for left in left_lines:
    for (x1,y1,x2,y2) in left:
        xs.extend([x1,x2])
        ys.extend([y1,y2])
A,B=np.polyfit(xs,ys,1)
start=(int((shape[0]-B)/A),shape[0])
end=(int((325-B)/A),325)
cv2.line(image,start,end,(0,255,0),3)

xs=list()
ys=list()
for right in right_lines:
    for (x1,y1,x2,y2) in right:
        xs.extend([x1,x2])
        ys.extend([y1,y2])
A,B=np.polyfit(xs,ys,1)
start=(int((shape[0]-B)/A),shape[0])
end=(int((325-B)/A),325)
cv2.line(image,start,end,(0,255,0),3)


cv2.imshow('image',image)
cv2.waitKey()