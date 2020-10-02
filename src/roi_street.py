import cv2
import numpy as np

rgb_threshold=[205,205,205]
image=cv2.imread('lanes.PNG')

left_bottom=(0,544)
center=(482,272)
right_bottom=(963,544)
img_width=image.shape[1]
img_height=image.shape[0]

color_threshold=(image[:,:,0]<rgb_threshold[0])|(image[:,:,1]<rgb_threshold[1])|(image[:,:,2]<rgb_threshold[2])

leftline_A,leftline_B=np.polyfit([left_bottom[0],center[0]],[left_bottom[1],center[1]],1)
rightline_A,rightline_B=np.polyfit([right_bottom[0],center[0]],[right_bottom[1],center[1]],1)
bottomline_A,bottomline_B=np.polyfit([left_bottom[0],right_bottom[0]],[left_bottom[1],right_bottom[1]],1)

XX,YY=np.meshgrid(np.arange(0,img_width),np.arange(0,img_height))
print(XX.shape,YY.shape)
region_threshold=((YY > (XX*leftline_A+leftline_B) )& (YY < (XX*bottomline_A+bottomline_B)) & (YY > (XX*rightline_A+rightline_B)))

# Show ROI in RED
#image[region_threshold]=[0,0,255]
lanes=image.copy()
#lanes[color_threshold]=[0,0,0]
lanes[~color_threshold & region_threshold]=[0,0,255]
cv2.imshow('',lanes)

cv2.waitKey()
