# Sensor Fusion for Object Tracking 

- [Sensor Fusion for Object Tracking](#sensor-fusion-for-object-tracking)
  - [Introduction](#introduction)
  - [How does Kalman filter works?](#how-does-kalman-filter-works)
  - [Fusion system architecture](#fusion-system-architecture)
    - [Kinematic model](#kinematic-model)
    - [Lidar measurement](#lidar-measurement)
    - [Radar measurement](#radar-measurement)
    - [Sensor fusion process](#sensor-fusion-process)
  - [Results analysis](#results-analysis)
  - [Reference](#reference)

## Introduction
The autonomous driving system consists of three main parts: perception, planning and control. The perception system is the basis of planning and vehicle control. In general, through the perception system, autonomous vehicles can obtain information from surroundings, like object detection and localization. In the previous project, the methods to identify objects in the images and videos taken by camera are introduced. However, the data collected by the camera is not always reliable since the camera doesn’t work in extreme condition. For example, the camera cannot find other vehicles in dense fog. More important, the camera cannot provide accurate information of distance and velocity of the obstacles, which is pretty important for the Obstacle Avoidance System and Adaptive Cruise Control. In this article, I will explain why the sensors of Lidar and radar can be used to track the objects and how to improve their performance with unknown environment by sensors fusion.   
Both Lidars and Radars are mounted on autonomous vehicles for obstacle detection. While Lidars are very accurate on obstacles positions and less accurate on their velocities, Radars are more precise on obstacles velocities and less precise on their position. In fact, accurate information of objects’ positions and velocities are critical for vehicles’ safety since they are essential for obstacle detection and tracking. One possible scheme is to combine the position data from Lidar and the velocity data from Radar to detect objects, like vehicles, pedestrians and animals. To some extent, it is a simple and practical way. However, autonomous vehicles have an extremely high requirement for the perception system. A minor error can lead to a collision which is never allowed. The accuracy of the data from sensors and the safety of vehicles are our profound pursuit. The sensors fusion takes advantage of the complementarity of sensors and is more robust to adverse conditions (weather, unavailability of one sensor). This article presents an introduction of the sensor fusion between Lidar and Radar and displays how the Kalman filter algorithm is implemented to improve the obstacle detection accuracy.  

## How does Kalman filter works?
Kalman filter algorithm is commonly used for state estimation and prediction. Here, I will not spend time to expand the principle of this algorithm. If you want to comprehend Kalman filter clearly, I recommend you this [website](https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/).[1]  
Before implementing the fusion of Lidar and Radar via Kalman filter, an issue should be noted. We usually focus on two parameters when tracking obstacle: the position P (including Px and Py)  and the velocity V (including Vx and Vy), and discuss the two parameters under Cartesian coordinates. While the data collected from Radar are expressed with three other parameters under polar coordinates, as shown in Figure 1.  
![Fig1)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Fig1.png)  
Figure 1 The measurement of Radar  
Although the position and velocity of obstacle cannot be read directly from the measurement of Radar, there is a nonlinear relationship shown in Equation (1) and (2):  
![Eq1)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq1.png)  
However, Kalman cannot be applied to process Radar data, since only when the system is linear system Kalman filter works. But don’t be worried! The extended Kalman filter (EKF), which is an advanced version of Kalman filter, can help us. More details about extended Kalman filter can be found from [here](https://www.cse.sc.edu/~terejanu/files/tutorialEKF.pdf)[2].  

## Fusion system architecture
### Kinematic model
In this section, the kinematic model of obstacle is established and the architecture of fusion system is built based on this model. When considering about obstacle tracking, two pairs of variables are essential:   
> 1)	x and y to describe the position of obstacle;  
> 2)	Vx and Vy to describe the velocity of obstacle.  
Consequently, the state vector of obstacle can be expressed by Equation (3):  
![Eq3)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq3.png)  
Assumed that the sampling period of sensors is T, thus the discrete state of obstacle at time k can be shown as:  
![Eq4)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq4.png)  
Here, ax and ay denote the acceleration of obstacle at x and y direction. For simplicity, we utilize constant velocity (CV) model, hence the value of ax and ay are zero. Equations (4) – (7) can be rewritten as:   
![Eq8)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq8.png)  
Equation (8) is a prior estimation of the obstacle’s state at time k, according to the kinematic model. Here, an additional variable v is added to describe the process errors, which can be introduced by the fluctuation of obstacle.  The prior estimation results are not reliable, since the value of v is not given in practice. Often, the process error v is assumed to be stochastic, and it has the following normal distribution:  
![Eq9)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq9.png)  
Now, we are trying to determine the value of Q.  
![Eq10)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq10.png)  
The process covariance is:  
![Eq11)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq11.png)  
Here, the variables ax and ay are not correlated, that means axy and axy are 0. Then, Equation (11) can be rewritten as:  
![Eq12)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq12.png)  
Due to the existence of process noise, the state estimation results through Equation (8) should be updated according to the measurement of Lidar and Radar. Now, let’s discuss separately.  

### Lidar measurement
Lidar can provide accurate information about the position of object, but not velocity of object. The observation equation of Lidar measurement is:  
![Eq13)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq13.png)  
Actually, the measurement of Lidar always has errors (also called measurement noise), which is a random variable. The value of measurement noise is not determined, and its covariance matrix Rl can be provided by the manufacturer.  

### Radar measurement
Different with Lidar, Radar can output the information of both position and velocity of obstacle. As described above, Radar does not provide the data of position and velocity directly, instead, it output the data under polar coordinates. In another word, it is difficult to express the relationship between the measurement of Radar and the state vector of obstacle via a simple linear matrix. The nonlinear function to connect this relationship is shown as follows:  
![Eq14)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq14.png)  
Even if the relationship is determined, the Kalman filter still cannot be applied to update the state vector since Kalman filter is only available for linear system. That’s why we choose extended Kalman filter.  
According to [2], a Jacobian matrix should be predefined by the following equation:  
![Eq15)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq15.png)  
Similarly, we assume that the measurement noise of Radar is zero-mean and it’s covariance is Rr.  

### Sensor fusion process
Now, we can update the estimation results of obstacle’s state vector according to the measurement of Lidar and Radar. The procedure is shown in Figure 2.  
![Fig2)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Fig2.png)  
Figure 2 Diagram of Sensor Fusion System  
Until now, everything is ready except one key element. According to the procedure shown in Figure 2, the value of covariance matrix P, Q, Rl and Rr should be determined in advance. Here, I want to talk about the determination of these matrix.  
> * Covariance matrix of estimation error P  
Matrix P denoted the covariance of estimation error, which can be updated through the previous time. Thus, what needed to be determined is the value of P0 at initial time. The matrix of P0 can be described by Equation (16):  
![Eq16)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq16.png)  
Usually, the initial state vector X0 of obstacle is set according to the Lidar measurement at initial time. That is:  
![Eq17)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq17.png)  
Therefore, the value of covariance of position is small than that of velocity. Here, we assume the value of P0 as shown in Equation (18) to represent this difference.  
![Eq18)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq18.png)  
> * Covariance matrix of process noise Q  
The covariance matrix of process noise Q has been deduced in Equation (9) – (12). Here, the value of process noise ax and ay are both set to be 1, for simplicity. As a result, the value of Q can be shown as:  
![Eq19)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq19.png)  
> * Covariance matrix of measurement noise Rl and Rr  
The value of Rl and Rr can be provided by the manufacturer. Here, I just give them an initial value. There is a major difference between Rl and Rr: the measurement of Lidar is 2D while the measurement of Radar is 3D. Consequently, the value of Rl and Rr are:  
![Eq20)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq20.png)  


## Results analysis
In this section, I will evaluate the estimation results of sensor fusion. The process of sensor fusion is implemented on MATLAB and the experimental data are provided by Udacity. In order to check the performance of sensor fusion, I use the root mean squared error (RMSE) and mean absolute error (MAE) to show how far the estimated results are from the ground truth. The lower value of RMSE and MAE means the higher accuracy of the estimated results. The computation of RMSE and MAE are shown in Equation (21):  
![Eq21)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Eq21.png)  
The RMSE of the estimated results of x, y, Vx and Vy are calculated and listed in Table 1.  
![Table1)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Table1.png)  
The MAE of the estimated results of x, y, Vx and Vy are calculated and listed in Table 2.  
![Table2)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Table1.png)  
As shown in Table 1 and Table 2, the RMSE of EKF is lower than that of Lidar, while does not have a clear difference compare to Radar. When it comes to MAE, the estimated results are more accurate than Radar’s measurement, but less accurate than Lidar’s measurement. However, the Lidar cannot provide the information of obstacle’s position. It is obviously that the estimated errors from EKF of obstacle’s velocity are lower than that of Radar, which means that we can obtain more accurate velocity information of obstacles.   
The trajectory of obstacle and the estimated results via sensor fusion is shown in Figure 3.  
![Fig3)(https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Sensor_Fusion_EKF/Graphs/Fig3.png)  
Figure 3 The trajectory of obstacle and the estimated results via sensor fusion  
In conclusion, we can get more accurate information about obstacle via the fusion of Lidar and Radar, which is pretty valuable to track objects and avoid accidents for autonomous vehicles.  

## Reference
> [1]	"How a Kalman filter works," https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/.  
> [2]	G. A. Terejanu. "Extended Kalman Filter Tutorial." https://www.cse.sc.edu/~terejanu/files/tutorialEKF.pdf. 


