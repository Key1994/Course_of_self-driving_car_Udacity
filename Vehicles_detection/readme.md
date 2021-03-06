# Introduction of Vehicle Detection Technology for Automatic Driving System  

[![Results](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig17.png)](https://www.youtube.com/watch?v=k1ELoOUojjs)  

- [Introduction of Vehicle Detection Technology for Automatic Driving System](#introduction-of-vehicle-detection-technology-for-automatic-driving-system)
  - [1. Introduction](#1-introduction)
  - [2. Vehicles detection based on features extraction and classifier](#2-vehicles-detection-based-on-features-extraction-and-classifier)
    - [2.1 Overview of the method](#21-overview-of-the-method)
    - [2.2 Extraction of HOG feature](#22-extraction-of-hog-feature)
    - [2.3 Train the classifier](#23-train-the-classifier)
    - [2.4 Sliding windows](#24-sliding-windows)
    - [2.5 Draw heatmap](#25-draw-heatmap)
    - [2.6 Display of detection results](#26-display-of-detection-results)
    - [2.7 Conclusion](#27-conclusion)
  - [3. Vehicles detection based on YOLO](#3-vehicles-detection-based-on-yolo)
    - [3.1 Introduction of YOLO](#31-introduction-of-yolo)
    - [3.2 Principle of the tiny YOLO](#32-principle-of-the-tiny-yolo)
    - [3.3 The design of loss function](#33-the-design-of-loss-function)
    - [3.4 Model training](#34-model-training)
    - [3.5 Results analysis](#35-results-analysis)
  - [4. Conclusion](#4-conclusion)
  - [5. References](#5-references)

## 1. Introduction
Vehicles detection is one of the most important tasks of unmanned vehicle’s perception system. Only by accurately identifying other vehicles around, the planning system can make decisions such as acceleration, braking, steering in time. Humans can easily identify the surrounding vehicles through the naked eyes without special training, but it does not mean that the computer can complete this task equally easily. Interestingly, existing artificial intelligence technologies tend to be good at the contrary of what humans are good at. For instance, the AI has outstanding advantages in the fields of big data analysis and calculation, information storage, but poor performance in logical judgment and unsupervised learning tasks, while human beings are just the opposite. Although the AI has achieved extensively applications in some fields at present, we are not satisfied with the status quo, so we are still exploring its application in many tasks.  
Our task is: the self-driving cars can detect the vehicles in pictures and videos, which are took by the cameras installed in cars. Furthermore, the detection should be accurate and fast to meet the practical requirement. “Accurate” means that the non-vehicle objects are not mistakenly identified as a vehicle. At the same time, all the vehicles can be detected. “Fast” is to emphasize the importance of recognition speed. When a car runs at a speed of 70km/h, it can go through nearly 20 meters per second. For the roads with large traffic flow (such as busy urban roads), there may be many vehicles in the 20-meter road, thus the unmanned car should recognize all these vehicles within a second. In addition, we also hope to improve the robustness of detection and reduce the cost of hardware as much as possible.  
When I search the keyword "vehicle detection methods" on Google, I find that this task has attracted the attention of many scholars, and a large number of publications are trying to solve it or improve the existing methods. Generally speaking, the existing methods can be divided into two kinds: traditional methods and intelligent methods.  
There are many kinds of traditional methods, such as appearance-based methods, and motion-based methods. These methods are simple in principle and low in computation. However, due to the variety of sizes and colors of cars, the accuracy of traditional methods cannot be guaranteed. In addition, different lighting conditions will also affect the recognition results, so traditional methods are gradually being replaced by intelligent methods.  
The intelligent methods detect and classify vehicles via intelligent algorithms, which usually consists of two parts. The first part is to use the feature description operator to extract image features (such as HOG features, Haar features). The second part is to judge that whether the features come from vehicles by the classifier. With the improvement of computer performance brought by the GPU, convolutional neural network and its improved forms have attracted wide attention due to their powerful capabilities in graphic feature expression. The YOLO and SSD methods proposed in recent years can detect the vehicles in an image without the process of segmentation of the images, which greatly improves the detection efficiency.  
In this article, I will realize the detection of vehicles via the feature extraction + classifier method and YOLO method respectively. And write the python codes to implement two methods to compare their detection results. Why these two methods? As mentioned earlier, traditional vehicle identification methods have gradually been replaced by intelligent algorithms due to their inaccuracy. The feature extraction + classifier method and YOLO are two typical representatives of the intelligent vehicle detection algorithm. Both methods have their own advantages, so a brief comparison between them is presented here.  

## 2. Vehicles detection based on features extraction and classifier  
### 2.1 Overview of the method  
This kind of method can be divided into two steps. First, the main features of the images are extracted by operators. For the computer, an image can be seen as a set of pixels or a matrix. Only by extracting the useful information from these pixels, the computer can try to “understand” this image. Then, we can train the classifiers by means of these features and detect objects in new pictures via the trained classifiers.  
The question is: what are the features that computers can easily "understand"? In fact, this question also attracts the attention of many scholars. The feature of histogram of oriented gradient (HOG) [1] proposed by Dalal in 2005 is a common feature in the field of object detection, such as pedestrian and vehicle. The HOG feature can describe images by computing and summarizing the histogram of gradient direction in the local areas. Another frequently-used feature is the Haar feature, which reflects the variation of the image’s grayscale. In addition, the information of scale-invariant feature transform (SIFT) and local binary pattern (LBP) are also frequently used to detect objects in the image. Here, I will take the HOG feature as an example to introduce what is HOG and how to use it in the vehicle detection.  
### 2.2 Extraction of HOG feature  
As the term implies, the HOG feature is a graphical display about the gradient directions. Thus, the gradient of each pixel should be calculated at the very beginning. Then, an image is divided into several cells and blocks. Drawing the histogram of the oriented gradient of each cell and summarizing the data of each histogram, the HOG features of the whole image can be obtained. More details can be found from [here](https://www.learnopencv.com/histogram-of-oriented-gradients/). Now, I will explain specifically how to extract the HOG feature of Figure 1, which contains 720 x 1280 pixels.  
![Fig 1 Example image](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig1.png)  
> Image preprocess  
>> * Convert the RGB image to grayscale, which is easier to calculate the gradient.  
>> * Normalization to improve the calculate accuracy. Here, I simply adjust the value of each pixel to the range from 0 to 1.0.  
Figure 2 is the image after preprocess.  
![Figure 2 Image after preprocess](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig2.png)  
> Calculate the gradient of each pixel  
The gradient of each pixel contains magnitude and direction. We can obtain the gradient magnitude of one pixel in the x direction (Gx) and y direction (Gy) respectively according to the adjacent pixel. Then, the actual gradient magnitude G and orientation alpha of this pixel can be calculated through the following equations:  
![Fig 15](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig15.png)  
> Drawing the histogram of oriented gradient  
In this step, the image is separated into several cells and each cell contains 8 * 8 pixels. Each pixel has two data: the gradient magnitude and gradient direction, thus a cell can be described by 8 * 8 * 2 = 128 data. The gradient direction of pixels is defined between 0 ~180 degree, so they are sorted in 9 bins in average here. The value of each bin is the sum of the gradient magnitude located in this bin. Once the value of each bin is determined, the histogram of oriented gradient can be drawn. Figure 3 is an example of a histogram.  
![Figure 3 Example of histogram](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig3.png)  
> Block normalization  
Due to the variation of local illumination and background contrast, the gradient intensity changes largely, so the normalization of local contrast is essential. The normalization is carried on the block, which is consist with several cells (for example, 2 * 2 or 4 * 4). There are 9 bins in a cell, means that a cell can be described by 9 data. In conclusion, if a block contains 2 * 2 cells it can be described by a vector with 2 * 2 * 9 = 36 elements. The relationship between pixel, cell and block is shown in Figure 4.  
![Figure 4 The relationship between block、cell and pixel](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig4.png)  
> Obtain the overall HOG feature of a image  
The example image shown in Figure 1 has 720 * 1280 pixels. If we choose the small block, the feature vector of the block will pay much attention on the local details of the whole image. Therefore, a block is set to be made up with 4 * 4 cells and its feature vector has 4 * 4 * 9 = 144 data. Take one block as a window, slide the window from the upper left of the image to the lower right and ensure that all the pixels in the image are covered, then the HOG feature of the whole image can be obtained.  
Actually, the HOG feature is not something enigmatic, instead it is just a way to describe the image gradient value. With this feature, the computer can understand the graphics more easily. Although the HOG feature extraction process is complicated, it can be implemented directly with the help of the provided function in Python.   
### 2.3 Train the classifier  
Once the HOG feature is extracted, we can use it to detect the objects in the image. First, the dataset for classifier training is required. Here, I use the [GTI](http://www.gti.ssr.upm.es/data/Vehicle_database.html) dataset which contains two subsets: the images with vehicles and images without vehicles. All the images in the dataset have 64*64 pixels. We can obtain the HOG features via the method mentioned in Section 2.2, and these features are used as inputs to train the classifier. There are many classifiers available here, such as the decision tree, support vector machine (SVM), K-mean algorithm, convolution neural network (CNN). The task here is just to identify the vehicles in the image, which is a common binary classification, thus the simple SVM classifier is adopted. It should be noted that if we need to solve a multi-objects detection task, for example, detect the cars, pedestrian, animals, traffic signs, the more sophisticated algorithms (such as CNN) should be considered.  
The SVM is a frequently used algorithm for classification, you can have a basic understanding of SVM from [here](http://www.saedsayad.com/support_vector_machine.htm).  
The procedure to train the SVM is:  
> * Annotating the images in the dataset and dividing them into training set and validation set, the ratio is 6:4.    
> * Extracting the images HOG features in the training set and validation set respectively through the method mentioned in Section 2.2. Integrating the features vector of each image.    
> * Fitting the relationship between features vectors and labels of each image in the training set, obtain the trained SVM model.  
> * Verifying the classification accuracy of the trained SVM model in the validation set. Here, I got a 95% accuracy in the validation set, so the performance of the trained model is satisfactory.  
> * Saving the parameters of the SVM model.  
### 2.4 Sliding windows  
The trained SVM model cannot be used to detect the vehicles in the example image in Figure 1 directly, since the images in the training set are 64*64, while the example image is 720*1280. In other words, the length of feature vector that SVM classifier expects and that of example image is inconsistent. To solve this problem, the method of sliding windows is applied.  
The principle of sliding windows is: select a box with fixed size and extract the HOG feature of this box. Using the feature vector of the box as the input of the trained SVM classifier and get the classification result. One box is a window, slide the window in the example image by a specific order until all the pixels are slid.  
The ideal size of the window is 64*64, which is consistent with the images in training set. However, the size of 64*64 is too small to contain the vehicle in the example image, thus the SVM cannot output accurate the results. In practice, the size of the window needs to be adjusted according to the size of the images taken by the camera. The pixels contain in a cell also need to be adjusted to ensure that the length of feature vector is appropriate.   
The selection of the window's sliding stride is also important. A small stride means that it needs more sliding windows to cover all the pixels and the computation will be larger. A large stride means that the sliding windows are too dispersive and the useful information may be ignored. Therefore, a reasonable sliding stride is a key factor for accurate vehicles detection.  
### 2.5 Draw heatmap  
I write the python codes to complete the steps in Section 2.2 and 2.3, and the vehicles detection result is shown in Figure 5. It can be seen that there are only 2 vehicles in the image, while too many windows claim that the vehicles are identified. The reason is that several adjacent windows may detect different portions of one vehicle at the same time. In fact, it is difficult to design a window to contain a vehicle entirely and other windows do not contain vehicles at all.  
![Figure 5 Vehicles detection result](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig5.png)  
Therefore, the redundant windows must be removed to ensure that a vehicle is corresponding to only a single window. A common method is to calculate the value of intersection over union (IoU) between windows. The IoU between two windows can be described by Figure 6.  
![Figure 6 The IoU between two windows](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig6.png)  
If the IoU between two windows is larger than certain threshold, it can be concluded that two windows have much area overlapped and they probably detect the same object. In this case, the window with higher score should be reserved and the window with lower score should be removed. What is the “score” here? When we adopt CNN as the classifier and use a softmax function in the last layer, then the CNN will output the probability that the object is a vehicle. The higher the probability is, the more accurate the result is. So, we can use the value of the probability as the score of the window. However, I use the SVM as the classifier here, which only output two results: the object is a vehicle or not a vehicle. The score is not available by the SVM model. Therefore, the primary task before calculate the IoU is to score all windows. I have tried many ways and finally use the heatmap.  
The procedure to draw a heatmap is as follows.  
> Step1：Define a matrix A with same shape with the example grayscale image, and all the elements are set to be 0;  
> Step2：Slide windows as mentioned in Section 2.4, and verify whether there is vehicles in the windows. If a window is classified to be negative, record the position (x,y,w,h) of this window and add 1 to all the elements contained by the rectangle (x,y,w,h) in matrix A;  
> Step3：When all the pixels in grayscale image are covered by sliding windows, set a threshold , find the elements in matrix A that are lower than , set these elements to be 0;  
> Step4：Call the positions of negative windows in step2, calculate the sum of all the elements in each window and save it as the score of this window;  
> Step5：Now, each window is scored. Find the window1 with maximal score, calculate the IoU between window1 and other windows. Remove the window whose IoU is larger than threshold;  
> Step6：Repeat step5 from the remained windows;  
> Step7：Repeat step5 and step6, until no windows remained. Then the selected windows with maximal scores in step5 are windows we need. Draw them in the raw image according to their positions (x,y,w,h).  
### 2.6 Display of detection results  
Here, I set the shape of window as 128*128, and the sliding stride is 32 pixels, the final detection result is shown in Figure 7.  
![Figure 7 Display of final detection result](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig7.png)  
### 2.7 Conclusion  
As shown in Figure 7, two vehicles in the image have been successfully detected. But there are still some problems. The left window does not contain the left vehicle entirely. In other words, the position of left window has some error. This problem can be solved by adding more windows in the image and decreasing the sliding stride. However, the two measurement will introduce another problem - the increase of computation. Thus, we must find a balance between the detection accuracy and computation. This is really a hot potato!  
In order to verify the vehicle detection results of the HOG + SVM method, I processed a 50s video via this algorithm, and the detection result can be viewed in this website.  

## 3. Vehicles detection based on YOLO  
Although the method based on features extraction and classifiers can detect the vehicles precisely, the balance between the accuracy and computation is difficult to achieve. When I try to detect vehicles in a 50-second video on my personal Macbook pro, it takes several hours. That’s unbelievable!   
Many scholars are devoted to find object detection method with higher speed. Among these methods, the method need only “one stage” is outstanding and the YOLO [2] and SSD [3] are the representatives. In this section, I will take the YOLO algorithm as the example to explain the principle of one-stage method.  
### 3.1 Introduction of YOLO  
YOLO is the abbreviation of “You Only Look Once”. To be honest, I don’t think this is a name of an algorithm when I first encounter this term. It was not until I have a deep understanding about this algorithm I am clear its ingenuity. As an “one-stage” algorithm, YOLO can detect the vehicles in an image and locate it without sliding window. Hence the large computation of sliding windows is avoided.  
The typical structure of YOLO is shown in Figure 8.  
![Figure 8 The structure of YOLO model](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig8.png)  
A completed YOLO model contains 26 layers. The first 24 layers are convolution layers, which are used to extract the main feature of images. The last 2 layers are fully-connected layers, which can output the probability of classification. The authors pretrained this model on the famous ImageNet 2012 dataset and fine tuned it on the PASCAL VOC 2007 and 2012 dataset. This model is pretty sophisticated and it takes a long time to train the parameters (about a couple of months on my laptop). Hence I use the faster version provided by authors – the tiny YOLO. The tiny YOLO is simplified to 9 convolution layers and 3 fully-connected layers.    
### 3.2 Principle of the tiny YOLO  
First, divide an image into an S*S grid, such as 7*7 and 13*13. If the center of an object falls into a grid cell, that grid cell is responsible for detecting that object. In fact, an object may locate in more than one cells, so it is important to determine the center of the object. For example, the image in Figure 9 is divided into 7*7 grid cells, the center of object “dog” locates in the 5th line, 2nd column cell. So, it is considered that cell is responsible to object “dog”.  
![Figure 9 The grid of the image](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig9.png)  
There are B bounding box (also called bbx) in a cell, which are used to described the probability and position of the objects. A bounding box is composed of 5 data: list (x,y,w,h) to describe the position and confidence to predict the class probability.   
The meaning of list (x,y,w,h) is shown in Figure 10. Generally, the value of four numbers are normalized to the range of [0,1].  
![Figure 10 The meaning of list (x,y,w,h)](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig10.png)  
The calculation of confidence is:  
![Fig 16](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig16.png)  
Pr(Object) is the probability that the bbx contains objects, which can be 0 or 1. Pr(Classi) refers to the probability that the object is i-th class if there is an object in the bbx.   
Therefore, the information of a cell can be expressed by a vector with (B * 5 + C) elements like Figure 11. Here, C is the number of the overall classes in the dataset.  
![Figure 11 The information vector of a cell](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig11.png)  
For an image, the final output dimension of YOLO model is S * S * (B * 5 + C)  
As mentioned previously, when detect vehicles via the method of “HOG + SVM”, we must slide windows to locate the object in the image. However, the YOLO can find the objects without sliding windows. Instead, the YOLO divides the image into several sections and detect the objects by locating the centers of objects.  
Another question is brought out: what is the function of the confidence in the bounding box? In fact, the classification results of the neural network always have some errors. For example, it is likely that there are many bounding boxes claim to be responsible to a same object. Similarly, we have to remove the redundant boxes via the IoU between the boxes just like what we do in Section 2.5. We have known that every score should have a “score” before using the IoU. In Section 2.5, I design the heatmap to score the windows, which is sophisticated. Here, we can use the confidence of each box as the score and use the common NMS (Non-Maximum Suppression) method to remove the redundant boxes. In addition, we can remove the boxes with lower confidence by setting a threshold since lower confidence means larger classification error.  
### 3.3 The design of loss function  
The design of loss function is indispensable for the model training. The following function is proposed in [2]:  
![Figure 12 The equation of loss function](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig12.png)  
### 3.4 Model training  
In this section, the details to train the tiny YOLO model will be presented. The work to prepare of the dataset and configure the parameters file are both complicated and time-consuming. But luckily, the authors of YOLO have opened the source code in their website. What we need to do is make some modifications according to our own task in the source code. The details are as follows.  
（1）Data preparation  
Here, I adopted the KITTI dataset, which provides more than 7000 images with detailed annotated information. But the dataset cannot be utilized directly because it is not applicable for the source code so I process the dataset as follows:  
> * The training in my own laptop is pretty time-consuming since there is no GPU. In order to shorten the training time, I just selected the first 3000 images to train the model.  
> * The objects in the KITTI dataset are divided into 8 classes: ‘Car’, ‘Van’, ‘Truck’, ‘Pedestrian’, ‘Person (sit- ting)’, ‘Cyclist’, ‘Tram’ and ‘Misc’. However, what I need to do is detect the vehicles in the example image, so I modified the classes in the annotated information. The images labeled ‘Car’, ‘Van’, ‘Truck’ and ‘Tram’ are relabeled as ‘car’, and the annotated information of images labeled ‘Person (sit- ting)’ and ‘Misc’ are deleted.   
> * The annotated information also need to be converted to the version that can be applicable for the source code. More details can be obtained from here.   
> * Split the training set, validation set and test set as 8:1:1.  
（2）Pretraining    
It takes time to train the model since there are too many layers and nodes (up to millions of parameters). A pretrained model is provided by the authors which can be loaded during the training to shorten the training epochs. However, the classification task is simple in this article, and there is a big difference between my dataset and that of author’s. Hence, I trained the model without loading pretrained model.  
（3）Train the model  
We can train the model by running the modified source code in a python complier. I initially set the epochs to be 30 and found that the detection results are not satisfactory due to overfitting. So I changed the epochs to 20 and took about 4 hours to train the model. The final result is shown in Figure 13.  
![Figure 13 The final detection result of tiny YOLO](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig13.png)  
### 3.5 Results analysis  
It can be seen that the two vehicles are perfectly contained by the boxes, and the boxes have a better accuracy in position and shape over the windows in Figure 7. Although the detection still has errors in some image - for example, the ‘cyclist’ is detected mistakenly in Figure 14 – we can remove the errors through a series of methods such as setting a threshold of confidence.  
![Figure 14 Another example of detection results](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Vehicles_detection/Graphs/Fig14.png)  
Moreover, considering the low computation of my computer, I just use a small dataset and a faster version of YOLO. So, it is confident that the detection can be more accurate if we increase the size of dataset and apply a more complicated model.  
I also test the vehicles detection results of tiny YOLO on the 50-second video, and it takes only 10 minutes to complete. What a improvement it is! The results can be viewed from [here](https://www.youtube.com/watch?v=k1ELoOUojjs).  
## 4. Conclusion  
In this article, two common-used vehicles detection methods on autonomous vehicle system are displayed. And the vehicles detection on a video has completed via these two methods.  
From the aspect of results, the method based on HOG + SVM and the method based on tiny YOLO can both find the position of objects and classify them correctly. Frankly speaking, the detection is not ideal. For instance, mistakenly classify the road as the vehicles or cannot detect the object in the environment with low light. However, we can improve the algorithm via many methods in the practical application. You can read relevant references if you are interested in.  
From the aspect of process, the two-stage method finds the object via the sliding windows, which are complicated and time-consuming; while the one-stage method can detect the objects from only one model which is faster to complete. Although the training of YOLO model needs a big dataset and powerful computer, I am confident that the one-stage method will have a better performance as the development of the computer’s processing capability.  
## 5. References  
[1]	 N. Dalal and B. Triggs, "Histograms of oriented gradients for human detection," in 2005 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR'05), 20-25 June 2005 2005, vol. 1, pp. 886-893 vol. 1, doi: 10.1109/CVPR.2005.177.   
[2]	 J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, "You Only Look Once: Unified, Real-Time Object Detection," in 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 27-30 June 2016 2016, pp. 779-788, doi: 10.1109/CVPR.2016.91.   
[3]  W. Liu, D. Anguelov, D. Erhan, C. Szegedy, S. Reed, C. Y. Fu et al., "SSD: Single Shot MultiBox Detector", in European Conference on Computer Vision, pp. 21-37, 2016.  







