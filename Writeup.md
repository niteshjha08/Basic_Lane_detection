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

![Hough lines](https://github.com/niteshjha08/Basic_Lane_detection/blob/master/writeup_images/hough6.PNG)
---
**draw_lines() function**

 To differentiate between lines belonging to the left and right lane, slopes and location of the lines can be used. Lines having a negative slope will belong to the left lane, and those having positive slope, to the right lane. (**Note**: This is opposite of the conventional slope which has signs the other way round. This is because the origin is at the top-left, not bottom-left.)
 
 However, there can be some misclassifications due to a similarly colored object on the road (or just random noise) if sign of slope was solely relied on. This can lead to terrible estimationes, as shown below.
 Lines detected as **left** are colored in **blue**.
 Lines detected as **right** are colored in **green**.

<img src="https://github.com/niteshjha08/Basic_Lane_detection/blob/master/writeup_images/only_slope_cause1.PNG" width="500" height="185"/>*Positive-slope line detected on left lane*

<img src="https://github.com/niteshjha08/Basic_Lane_detection/blob/master/writeup_images/only_slope_error_result1.PNG" width="500" height="260"/>*Incorrect result due to this*

 
To account for this, lines are also checked for their  x-coordinates. Lines on the first half of the image will correspond to the left lane, and those in the second half will correspond to the right lanes.

![line_segments](https://github.com/niteshjha08/Basic_Lane_detection/blob/master/writeup_images/line_segments.PNG)


Only when both these conditions are satisfied (slope and location), points are appended to a list of respective lanes, and final aggregated slope and intercept is calculated for both lanes, and plotted on original image after blending for transparency.

![Hough lines](https://github.com/niteshjha08/Basic_Lane_detection/blob/master/writeup_images/hough6.PNG)



### 2. Potential shortcomings 

One potential shortcoming to this pipeline could be when a left lane is actually in the right part of the image, in which case it will fail to detect. This can happen in tight corners.

Another shortcoming could be when there are various marking on the road of colors similar to the lanes, such as pedestrian crossings (or crosswalk). Due to large amount of lines throughout the breadth of image, it might give bad estimates.

Moreover, even mildly congested areas, with cars close by, can distort the results significantly.
### 3. Possible improvements to the pipeline

A possible improvement would be to determine optimum values of slope which can successfully differentiate left and right lane lines out of the many lines detected by Hough transform. This will help in getting rid of the first shortcoming mentioned above, i.e. location would not be an issue then.

Sophisticated methods of lane extraction, such as CNNs would help in making it robust to nearby traffic and lane markings.

Moreover, a limiting element can be put which restricts change of final lane line's slope by a significant margin quickly, as lanes generally change slope gradually. This will ensure erratic fluctutations. 

