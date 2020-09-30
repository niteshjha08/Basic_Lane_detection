import cv2
import numpy as np
import math

cap=cv2.VideoCapture('test_videos/solidWhiteRight.mp4')
while(cap.isOpened()):
    ret,image=cap.read()
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
    canny=cv2.Canny(img,50,150)

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

    ####################################################################################
    #              Method 1:
    ##################################################
    # xs=list()
    # ys=list()
    # for left in left_lines:
    #     for (x1,y1,x2,y2) in left:
    #         xs.extend([x1,x2])
    #         ys.extend([y1,y2])
    # A,B=np.polyfit(xs,ys,1)
    # start=(int((shape[0]-B)/A),shape[0])
    # end=(int((325-B)/A),325)
    # cv2.line(image,start,end,(0,255,0),3)
    #
    # xs=list()
    # ys=list()
    # for right in right_lines:
    #     for (x1,y1,x2,y2) in right:
    #         xs.extend([x1,x2])
    #         ys.extend([y1,y2])
    # A,B=np.polyfit(xs,ys,1)
    # start=(int((shape[0]-B)/A),shape[0])
    # end=(int((325-B)/A),325)
    # cv2.line(image,start,end,(0,255,0),3)
    ##################### END OF METHOD 1 #####################
    left_slope=0
    left_c=0

    # delete this block after correction
    # for left in left_lines:
    #     for (x1, y1, x2, y2) in left:
    #         cv2.line(image,(x1,y1),(x2,y2),(255,0,0),2)
    # cv2.imshow('linecheck',image)
    # cv2.waitKey()
    #
    # for right in right_lines:
    #     for (x1, y1, x2, y2) in right:
    #         cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
    # cv2.imshow('linecheck',image)
    # cv2.waitKey()
    ### ending here ####


    for left in left_lines:
        for (x1,y1,x2,y2) in left:
            del_left_slope,del_left_c=np.polyfit([x1,x2],[y1,y2],1)
            left_slope=left_slope+del_left_slope
            left_c=del_left_c+left_c
            #left_slope=left_slope+(y1-y2)/(x2-x1)    # Note difference in formula, as y is downwards.
            #print(left_slope,(x1,y1),(x2,y2))
            #left_c=(shape[0]-y2-left_slope*x2)


    right_slope = 0
    right_c=0
    for right in right_lines:
        for (x1, y1, x2, y2) in right:
            del_right_slope, del_right_c = np.polyfit([x1, x2], [y1, y2], 1)
            right_slope = right_slope + del_right_slope
            right_c = del_right_c + right_c
            # right_slope = right_slope + (y2 - y1) / (x1 - x2)
            # right_c =shape[0]- y2 - right_slope * x2

    # finding mean of slopes and intercepts
    left_slope=left_slope/len(left_lines)
    right_slope=right_slope/len(right_lines)
    left_c=left_c/len(left_lines)
    right_c = right_c / len(right_lines)
    print('right data')
    print(right_slope,right_c)

    # finding end points of desired lane line for drawing
    left_start=(int((shape[0]-left_c)/left_slope),shape[0])
    print(left_start)
    left_end=(int((325-left_c)/left_slope),325)
    print(left_end)
    right_start=(int((shape[0]-right_c)/right_slope),shape[0])
    right_end = (int((325 - right_c) / right_slope), 325)
    print('right points')
    print(right_start)
    print(right_end)
    cv2.line(image,left_start,left_end,(255,0,0),2)
    cv2.line(image, right_start, right_end, (0, 255, 0), 2)



    cv2.imshow('frame',image)
    cv2.waitKey(33)