# The project of lane lines finding 

[![Video1](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/lane_lines_finding/Graphs/cover1.png)](https://www.youtube.com/watch?v=C8_XqO329_k)  

## Introduction  
Vehicles need to follow certain driving rules. It is the lane lines on the road plays the role in regulating the driving rules of vehicles. There are many kinds of lanes, such as single-lane, double-lane, dashed line, grid line, etc. Lane lines of different colors also represent different driving rules. Cars and pedestrians can use the lanes to avoid conflicts. Therefore, accurate detection and recognition of lane lines are the basis of automobile driving.  
The course of self-driving car Udacity includes a lane lines' detection project, whose purpose is to teach vehicles how to detect and identify lanes. This document summarizes the contents of this project.  
There are two main method to finding lane lines in the picture.   
> * Lanes detection based on road characteristics;   
> * Lanes detection based on road model. 

![Fig1](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/lane_lines_finding/Graphs/Fig1.png)  
The first method uses the difference of physical characteristics between lanes and road environment to segment and process images, so as to highlight lane features and realize lane detection. This method has low complexity and high real-time performance, but it is vulnerable to road environment interference. The second method bases on different road models (such as straight line, parabola, spline curve, combination model, etc.), and determine the parameters of each model via proper methods. This method has high accuracy for the detection of specific roads, but it has strong limitations, such as large computational complexity and poor real-time performance.  
In this project, the lanes detection method based on road characteristics is adopted. The main processes are as follows.  
### Image transform  
The photos taken by the automobile's camera are RGB graphics with three-channel.In order to extract the gray-scale features of these graphics, it is necessary to convert them into single-channel gray images. The opencv toolkit in Python can be used to implement this transformation. The codes used are as follows:  
```Python  
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
```
The left image is the original RGB image captured by the camera, and the right image is the gray image after transformation.   

### Edge extraction  
In the computer, the gray image can be regarded as a matrix composed of pixel values. The pixel values are integers between 0 and 255. Specificly, if the color of one point in the image is black, the pixel value of this point is set to be 0, and the pixel value of white point is set to be 255. However, such data sets are too complicated to be understood by the computer, so this section tells how to extract the edges of graphics.  
The purpose of edge extraction is to find out the contour features of each object in a graph. The Canny method is used to complete the edge extraction of graphics in this project, which contains following steps:  
![Fig2](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/lane_lines_finding/Graphs/Fig2.png)  
The module of noises elimination is used to remove noise points in graphics to avoid these points being recognized; The calculation of pixel gradient is the core of Canny algorithm, which calculates the gradient values to judges the color variation in graphic; The unreal edges can be removed through non-maximum suppression module, and only the pixels that are most likely to be edges can be retained; Finally, two hysteresis thresholds are set to enhance the accuracy of lane detection. The following figure is the image after the edge extraction. It can be seen that the object contour and edge lines are described, which looks more concise and is easier to be understood by computer.   
![Fig3](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/lane_lines_finding/Graphs/Fig3.png)  
### The determination of ROI (region of interest)
Although the lines and contours in the original image have been depicted, we should always remember the purpose of the project: detection of lane lines!  
That is to say, all parts of the figure except the lane lines are not the objects we are interested in. Therefore, we can select a specific area as the region of interest (ROI). The lines outside the ROI are removed.  
Here one question comes: Is it indispensable to select ROI? The answer is no. However, by determining ROI we can greatly reduce computation.  
Another question is: how to choose ROI?  
There is no fixed answer to this question. For example, in this project, we assume that the camera used for image acquisition is installed in the middle of the front of the car. In most cases, the vehicle travels between two adjacent and parallel lanes (unless it needs to change lanes), so we can regard that the ROI can be selected in the middle of the graph.  
The shape of ROI is not unique, we can choose triangles, rectangular frames, circles, ellipses, irregular polygons and so on, it depends on the actual needs of. For simplicity, triangles are used as the ROI in this project. The position of the triangle in the original picture is shown as follows:  
![Fig4](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/lane_lines_finding/Graphs/Fig4.png)  
According to the shape and position of the ROI, we can write rigion_of_interest function to remove the lines outside ROI. Only the lines inside the ROI can be retained. The final filtered figure is:  
![Fig5](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/lane_lines_finding/Graphs/Fig5.png)  
It can be seen that the graphic has been greatly simplified.  
### Hough transform
So far, the original RGB graphics captured by cameras have been simplified step by step. There is another problem that needs to be solved here. Computers can calculate the slope of the lines and draw lines according to the value of slope and intercept. However, if there is a lane line perpendicular to the horizontal axis, then its slope tends to be infinite, which is impossible for computer to calculate and draw.  
In order to solve this problem, Hough transform is introduced. Readers can easily find relevant information from the Internet, so the principle of Hough transform is no longer discussed here. In a word, Hough transform mainly solves the problem of infinite slope of lane lines. There is a module in python called opencv which can directly complete the Hough transform of graphics. The code of function call is as follows:  
```Python
img_hough = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength,maxLineGap)  
```
In this function, "img" is the figure that needs Hough transform; "Rho" and "theta" are the resolution of distance and angle respectively; "threshold" controls the minimal number of points in a line; "minLineLength" is the minimal length of a line, that is to say, it is only when the length is greater than minLineLength, the line is marked; "maxLineGap" is the maximal distance between two points in a line. If the distance between two points is greater than maxLineGap, it can be regarded that these two points do not belong to the same line. After Hough transform, the figure is as follows:  
![Fig6](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/lane_lines_finding/Graphs/Fig6.png)  
In this example, there is no infinite slope of lane lines, thus there is no difference between the images before and after hough transformation.   
### Drawing lane lines
Now, the lane lines in the graph has been detected. In this section, the lane lines will be depicted on the original picture in order to validate the detection result:  
![Fig7](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/lane_lines_finding/Graphs/Fig8.png)  
As you can see in the picture above, the lane lines have been identified obviously!  
Due to the determination of ROI, the lanes far from the camera were not marked. But don't worry, the lanes are recognized in real time during the driving process, so the lane can be detected and drawn continuously.  
In order to further verify the effectiveness of this method, another picture is processed and the detection result is as follows:  
![Fig8](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/lane_lines_finding/Graphs/Fig8.png)  
It can be verified in this example that this method can detect the lane lines perfectly.   

## Lane lines detection for video
The above sections tells a lane detection method for single image. In practical application, real-time lane detection is needed for vehicles driving to avoid deviating from the lane. The information captured by the vehicle's camera is often presented in the form of video, so it is necessary to recognize the lane lines in the video. It sounds a bit complicated, but don't worry at all. The video can be seen as the superposition of multiple pictures, so we only need to divide the video and extract every picture. Then the lanes detection method for single image can be used.   
Of course, it is difficult for novices to process a video and extract the images. Here I must commend the powerful video process tool in python -- Video FileClip module. We just need to call this function according to the established rules, the extraction of pictures from a video can be completed. Then we can use the lane lines detection method for single image to process each picture. The following codes tell how to use the Video FileClip module in python. "example1_output" is the address of the processed video stored on my personal computer; the address behind "Clip1" is the address of the processed video.  
```Python
example1_output = '/Users/zhangzheng/Desktop/lane_lines_finding/test_videos_output/solidWhiteRight1.mp4'  
clip1 = VideoFileClip("/Users/zhangzheng/Desktop/lane_lines_finding/test_videos/solidWhiteRight.mp4")  
print clip1  
example1_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!  
%time example1_clip.write_videofile(example1_output, audio=False)  
```

## Improvement
In this project, another video named "challenge.mp4" -which can be found in this folder - is provided. In the video, there are lots of shadows and the road surface is damaged, which will influence the accuracy of the lanes detection. The video is processed via the method in above section, and the result can be seen in the file named "challenge-output.mp4". From the video, it can be seen that in the time interval of 3-6 seconds, the road lines detection results are very unsatisfactory, mainly as follows:  
> * The shadows of the trees' branch on the road are misidentified as road lines;  
> * Identify the front edge of the vehicle as a road line;  
> * In the rigion where the road surface is damaged, the road lanes can not be identified.   
These problems will seriously affect the safety of the self-driving cars, so we need to find ways to solve them.  
### Increasing the threshold of Canny function
When calling Canny function in Python, we need to input two thresholds. When the gradient value of a pixel is smaller than the minimum threshold, the pixel is eliminated; when the gradient value is larger than the maximum threshold, the pixels are retained; when the gradient value is located between the two thresholds, it is considered separately. Therefore, by increasing the two thresholds at the same time, the small gradient of pixels can be removed, thus eliminating the shadows of the trees' branches on the road, because the gradient of these shadows is often smaller than the gradient of the lane.  
### Converting Yellow Line to White Line
In the damaged part of the road, the lane line can not be recognized because the difference between the yellow lane lines and the road surface is not obvious. That is, the gradient value of the pixels on the lane line is not large enough to be retained. In order to solve this problem, we first write a function to convert the yellow line to the white line to improve the gradient value of the pixels on the lane lines, so as to improve the probability of the detection of the lanes. The function code is as follows:  
```Python
def yellow_transform(image):  
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  
    lower_yellow = np.array([40, 100, 20])  
    upper_yellow = np.array([100, 255, 255])  
    mask = cv2.inRange(image_hsv, lower_yellow, upper_yellow)  
    return mask  
```
### Results validation
Once the improvements are completed, we verify the results on the video named "challenge. mp4". In order to make the effect more obvious, the original video is processed here to make it darker so that the detected lane lines can be easily observed on the graph.  

[![Video2](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/lane_lines_finding/Graphs/cover2.png)](https://www.youtube.com/watch?v=sNm08lyf_6I)  

It can be seen that most of the trees' shadow are ignored after the improvement. In the damaged part of the road, some lane lines can be detected. Although the results are still not perfect and many problems also exist, it has been significantly improved compared with the original results. Therefore we can consider that our improvement method is effective. However, the improving section will increase the amount of calculation and the operation time, which requires stronger processor to complete the operation. This is a disadvantage of the improved method.  
