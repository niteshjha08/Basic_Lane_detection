import cv2
import numpy as np
import matplotlib.pyplot as plt
print('running')
image=cv2.imread('lanes.PNG')
rgb_threshold=[205,205,205]
img_width=image.shape[1]
img_height=image.shape[0]
line1=
roi=image[img_height/2:,:]
threshold=(image[:,:,0]<rgb_threshold[0])|(image[:,:,1]<rgb_threshold[1])|(image[:,:,2]<rgb_threshold[2])
copy_img=image.copy()
copy_img[threshold]=[0,0,0]

cv2.imshow('',copy_img)
cv2.waitKey()

