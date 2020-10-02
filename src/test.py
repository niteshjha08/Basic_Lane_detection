import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2



import math


def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    # defining a blank mask to start with
    mask = np.zeros_like(img)

    # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    # returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).

    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    copy1=image.copy()
    lx = []
    ly = []
    rx = []
    ry = []
    i = 0
    for line in lines:

        for (x1, y1, x2, y2) in line:
            slope = ((y2 - y1) / (x2 - x1))
            if (slope<0):  # Left lane line
                lx.extend([x1, x2])
                ly.extend([y1, y2])
                cv2.line(image,(x1,y1),(x2,y2),(255,0,0),2)
            if (slope>0):  # Right lane line
                rx.extend([x1, x2])
                ry.extend([y1, y2])
                cv2.line(image, (x1, y1), (x2, y2), (0,255,0), 2)
    left_A, left_B = np.polyfit(lx, ly, 1)
    left_start = (int((shape[0] - left_B) / left_A), shape[0])
    left_end = (int((325 - left_B) / left_A), 325)

    right_A, right_B = np.polyfit(rx, ry, 1)
    right_start = (int((shape[0] - right_B) / right_A), shape[0])
    right_end = (int((325 - right_B) / right_A), 325)

    cv2.line(copy1, left_start, left_end, (0, 0, 255), 10)
    cv2.line(copy1, right_start, right_end, (0, 0, 255), 10)
    cv2.imshow('individual_lane_lined',image)
    cv2.imshow('overall_result', copy1)
    #final=cv2.addWeighted(image,0.6,copy,0.4,0)
    #cv2.imshow('slopemethod',final)


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img


# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.

    `initial_img` should be the image before any processing.

    The result image is computed as follows:

    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)

cap=cv2.VideoCapture('./../test_videos/solidYellowLeft.mp4')

while(cap.isOpened()):
    ret,image=cap.read()
    img=image.copy()
    copy=image.copy()
    red_thresh = 220
    green_thresh = 180
    blue_thresh = 70
    rgb_thresh = [blue_thresh, green_thresh, red_thresh]

    color_threshold = (image[:, :, 0] < rgb_thresh[0]) | (image[:, :, 1] < rgb_thresh[1]) | (image[:, :, 2] < rgb_thresh[2])

    img[color_threshold] = [0, 0, 0]
    #image = cv2.imread('test_images/solidWhiteRight.jpg')
    gray=grayscale(img)

    cannyimg=canny(gray,50,150)

    shape=image.shape

    vertices=np.array([[(48,shape[0]),(422,324),(538,324),(shape[1],shape[0])]],dtype=np.int32)
    roi=region_of_interest(cannyimg,vertices)
    cv2.imshow('roi',roi)
    lines=hough_lines(roi,2,math.pi/180,5,20,40)
    cv2.waitKey()