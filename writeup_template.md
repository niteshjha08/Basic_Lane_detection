# **Finding Lane Lines on the Road** 

---


The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on the work and determine limitations, along with potential improvements


---

### Reflection

### 1. Describe the pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 steps.
 
![Original_Image](https://github.com/niteshjha08/Basic_Lane_detection/blob/master/writeup_images/original.PNG)

*Original Image*
1. **Color Thresholding** : Based on optimum values obtained from [lane_finding_tuner](https://github.com/niteshjha08/Basic_Lane_detection/blob/master/src/lane_finding_tuner.py), the R,G,B values are determined which only keep the key regions of image (along with a little noise), i.e. lane lines, making other regions  black.
![Color_thresholding](https://github.com/niteshjha08/Basic_Lane_detection/blob/master/writeup_images/color_threshold.PNG)

*Output of color thresholding*

2. **Grayscaling** : The output of previous step is then grayscaled. 
![Grayscale](https://github.com/niteshjha08/Basic_Lane_detection/blob/master/writeup_images/grayscale3.PNG)

*Output of grayscaling*

3. **Canny edge detection** : Then, the edges of this grayscale image is detected.
![Canny](https://github.com/niteshjha08/Basic_Lane_detection/blob/master/writeup_images/canny4.PNG)

*Output of canny edge detection*

4. **Region masking** : Keeping in mind the occurrence of lane lines in general, vertices of region of interest are determined, and a mask is created, which is white inside these ROI, and black elsewhere. Then, a bitwise_and operation takes place between this mask and canny edges from the previous step. This results in an image with edges only in the ROI, eliminating all edges in other regions. 
![Region_masking](https://github.com/niteshjha08/Basic_Lane_detection/blob/master/writeup_images/roi5.PNG)

*Output of region-masking of canny edges*

5. **Hough lines** : Finally, the lines are detected in only the edges in the ROI, i.e. output of previous step, with hough parameters obtained.
---
**draw_lines() function**

 To differentiate between lines belonging to the left and right lane, slopes and location of the lines can be used. Lines having a negative slope will belong to the left lane, and those having positive slope, to the right lane. (**Note**: This is opposite of the conventional slope which has signs the other way round. This is because the origin is at the top-left, not bottom-left.)
 
 However, there can be some misclassifications due to a similarly colored object on the road (or just random noise) if sign of slope was solely relied on. This is shown below.
 Lines detected as **left** are colored in **blue**.
 Lines detected as **right** are colored in **green**.

 ![error1](https://github.com/niteshjha08/Basic_Lane_detection/blob/master/writeup_images/only_slope_error_cause1.PNG)    ![result1](https://github.com/niteshjha08/Basic_Lane_detection/blob/master/writeup_images/only_slope_error_result1.PNG)

 
In addition to slope, lines are also checked for their  x-coordinates. Lines on the first half of the image will correspond to the left lane, and those in the second half will correspond to the right lanes. Only when both these conditions are satisfied (slope and location), points are appended to a list of respective lanes, and final aggregated slope and intercept is calculated for both lanes, and plotted on original image after blending for transparency.

![Hough lines](https://github.com/niteshjha08/Basic_Lane_detection/blob/master/writeup_images/hough6.PNG)

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]


### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...
