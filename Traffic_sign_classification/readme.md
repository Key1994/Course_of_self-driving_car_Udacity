# Traffic Sign Classifier

## Introduction
It is an important premise to make the autonomous vehicles have the ability of traffic sign recognition to ensure that the vehicles drive according to the correct traffic rules. There are two main methods to recognize the traffic sign. The first method is to write the information of traffic signs into the high precision map and read them in according to the vehicles’ position. The implementation of this way has some limitations, such as the highly accurate positioning of vehicles and regular update of high precision map. Another method is to classify the traffic signs on the images took by the cameras, that is the recognition based on computer vision.  
In this project, I will classify traffic sign images via the second method. A convolution neural network is trained on the [German Traffic Sign Dataset](benchmark.ini.rub.de/?section=gtsrb&subsection=dataset).  

![Figure 1 A preview of the images in GTSD](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Traffic_sign_classification/Graphs/Fig1.png)  

## Implementation
### Load The Data
There are 43 classes of traffic sign in the dataset and the sample size of training set, validation set and test set are 34799, 4410 and 12630, respectively. The size of each image is 32 * 32. The pickled data is a dictionary with 4 key/value pairs:  
> * 'features': is a 4D array containing raw pixel data of the traffic sign images, (number of examples, width, height, channels).  
> * 'labels': is a 2D array containing the label/class id of the traffic sign. The file signnames.csv contains id -> name mappings for each id.  
> * 'sizes': is a list containing tuples, (width, height) representing the original width and height the image.  
> * 'coords': is a list containing tuples, (x1, y1, x2, y2) representing coordinates of a bounding box around the sign in the image.  

### Image process
> * Normalize the dataset to (0,1): X = (X – X_min) / (X_max – X_min)  
> * Convert the RGB image to grayscale  

### Make one-hot code according to the labels
The format of labels looks like: [16 12 1 28 23 ….]. The label of an image is a number, which refers to the index of the classes. Here the label should be converted to the format of one-hot code to be consistent with the output of the neural network. The format of one-hot code looks like:  
[0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]  
[0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]  
[0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]  
[0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]  
[0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]  
Now, the label of an image is a vector with 43 elements. If a traffic sign is i-th class, the i-th element of the vector is set to be 1, other elements are 0.  

### Establish the structure of the neural network and train it.
The famous LeNet[1] model is applied here, whose structure is shown in Figure 2.  
![Figure 2 The structure of the LeNet model](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Traffic_sign_classification/Graphs/Fig2.png)
The specific parameters of each layers are:  
![The specific parameters of each layer](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Traffic_sign_classification/Graphs/Table1.png)
Establish the model in Keras and train it on the training set. The setting of model can be found in Section 2.  

### Validate the classification results of the trained model.
The classification accuracy of the LeNet model is validated on the validation set and the results are recorded in Section 2.  

## Results
The classification accuracy is recorded under different parameters, such as epochs, batch size and learning rate. Now, I will explore how to determine the proper value of these parameters.  
### Epochs
The LeNet model is trained with 10, 20, … , 70 epochs respectively, the learning rate and batch size are set to be 0.001 and 64 simply. The classification accuracy on the validation set of the trained model is recorded on Figure 3.  
![Figure 3 The relationship between the classification accuracy and epochs](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Traffic_sign_classification/Graphs/Fig3.png)
It can be concluded that the accuracy increases as the increase of training epochs. When training epoch is more than 50, the accuracy no longer improves, which means that the model may be overfitted. Hence, the epochs here is set to be 50.  

### Batch size
The value of batch size controls the number of samples input to the model at one time. Big batch size always increases the computation, while small batch size is likely to influence the performance of the model. According to the description in book “Deep Learning” written by Ian Goodfellow and Yoshua Bengio, the value of batch size is often set to be the power of number 2 ranging from 32 to 256. Here, the classification accuracy with the batch size of 32, 64 and 128 are verified.   
As shown in table 1, the classifier has the best performance when the batch size is set to be 64.  
![The relationship between batch size and accuracy](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Traffic_sign_classification/Graphs/Table2.png)
### Learning rate
The learning rate is another important factor affecting the classification accuracy. The initial learning rate is set to 0.001 and the values around initial value are also verified. The results are plotted on Figure 4.  
![Figure 4 The relationship between the classification accuracy and learning rate](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Traffic_sign_classification/Graphs/Fig4.png)
As shown in Figure 4, the accuracy will decrease when the learning rate is more than or less than 0.001. Therefore, the value of 0.001 is considered to be the best selection.  

## Summary
In this article, the traffic sign classification method via neural network is introduced. The significance of this project is described and the famous LeNet model is established. Through continuous fine tuning, the optimal value of model parameters is obtained, and the classification accuracy of the trained model is more than 92.9% finally.  
However, there are still some aspects can be improved.  
Firstly, the position of the traffic sign in the image has been determined in the German Traffic Sign Dataset, which is impractical when we test in the actual application. The solution of this problem is similar to the method of vehicles’ detection. We can firstly locate the traffic signs on the image and then classify them through the neural network trained in this article, that is the so-called two-stage method. Another method is the one-stage method, such as YOLO or SSD.  
Second, the LeNet is a classical but simple convolution neural network, which is suitable for beginners. If we need to further improve the classification accuracy, a more complicated model is needed.  
Last but not least, even if the position of the traffic sign in an image is certain, many factors can also affect the classification. For example, the signboard may become deformed due to the collision or sheltered by the branches. In order to reach a higher recognition accuracy, the combination of methods based on the camera and methods based on high precision map is a better conception.  

## References
Y. Lecun, L. Bottou, Y. Bengio, and P. Haffner, "Gradient-based learning applied to document recognition," Proceedings of the IEEE, vol. 86, no. 11, pp. 2278-2324, 1998, doi: 10.1109/5.726791.  
