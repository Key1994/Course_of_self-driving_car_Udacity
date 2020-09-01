# Robot Localization via Particle Filter

- [Robot Localization via Particle Filter](#robot-localization-via-particle-filter)
  - [Introduction](#introduction)
  - [Localization model](#localization-model)
  - [Implementation of particle filter](#implementation-of-particle-filter)
    - [Generating particles](#generating-particles)
    - [Measurements](#measurements)
    - [Importance weight](#importance-weight)
    - [Resample](#resample)
  - [Results analysis](#results-analysis)
    - [Errors under different number of particles](#errors-under-different-number-of-particles)
    - [Errors after iterations](#errors-after-iterations)
  - [Conclusion](#conclusion)
  - [References](#references)

## Introduction
The problem of localization is one of the most fundamental issues for mobile robotics. Accurate localization not only is essential for other tasks, like path planning and control system, but also provide a guarantee to avoid collision. The robot can be localized locally or globally depending on different methods. Local techniques aim at compensating odometrical errors occurring during robot navigation, while global techniques are designed to estimate the position of the robot even under global uncertainty[1]. In addition, the local localization needs the initial position of robot to track it. However, the global localization can solve the so-called wake-up robot problem, in that the robot can be localized without any prior knowledge about the initial position. Obviously, the global location techniques are more powerful than local ones as they can find the robot from scratch, as a result many references have worked on this problem.  
In this project, the particle filter is applied to realize the global localization for robots. PF implements recursive Bayesian filter based on Monte Carlo simulation and it shows merits in dealing with nonlinear and non-Gaussian models. The particle filter is always compared with Kalman filter, which can also be utilized to eliminate the influence of uncertainty, i.e., process noises and measurement noises. However, the Kalman filter assuming that the kinematic model of the robot is linear, otherwise the algorithm will face failures. The extended Kalman filter (EKF) and unscented Kalman filter (UKF) can be used to handle the non-linearity of robot kinematic model, while they are only effective when the uncertainty is Gaussian. Instead, the particle filter can cope with non-linear system and non-Gaussian uncertainty, consequently is more powerful to localize the robot globally.   
In this article, a simple localization model will be established firstly, the principle of particle filter is introduced afterwards based on this model. In order to verify the localization accuracy, the particle filter is programmed with Python. Finally, I will analyze the results and summarize the strengths and weaknesses of particle filter.  

## Localization model
In reality, if we are lost in a new place and we don’t have a device, like GPS or digital map, to localize ourselves, what’s the best way to collect the knowledge of actual position? Yes, landmarks! For example, if we see the Eiffel Tower in front of us then it can be convinced that we are in Paris, or even more specific address. The global localization of robot is in the same way.   
Here, the model space is set to be 100*100, inside which four points with definite positions are set as landmarks. As shown in Figure 1, the coordinates of four landmarks are (20, 20), (20, 80), (80, 20), and (80, 80) respectively. The mobile robot is located in the map initially and randomly, and move by specific yaw angle  and distance. In theory, the robot can be localized precisely by measuring the distance from four landmarks. That’s pretty simple! However, due to the existence of noise, the exact values are unavailable. That’s what the problem is in practical reality.  
![Figure 1. Diagram of the localization model](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Localization_particle_filter/Graphs/Fig1.png)  

## Implementation of particle filter
The particle filter is usually utilized for estimation or localization due to its high robustness against uncertainty and noise. The particle filter can be implemented by following steps.  

### Generating particles
At the very beginning, the information of the robot’s position is unknown, hence we assume that the distribution is uniform. In other words, we consider that the robot has the same probability to locate at anywhere in the space. The question is, how to represent this distribution?
One possible solution is to select a point randomly in the map and adjust the position gradually with iterations, just as how Kalman filter works. But this method has a large bias so it takes a long time to converge to the exact point. Another technique is to create a set of points uniformly to represent the distribution of the initial position. Although most of the points are not accurate, we can obtain some points locating nearby the exact point. What we need to do is to find these ideal points to represent the exact position. That is how particle filter works.   
The regulation to create the N particles is in line with the distribution of the initial value, here it is uniform distribution. As shown in Figure 2, the blue circle points denote the particles generated randomly (N = 1000), while the point marked with red “x” denotes the exact value.  
![Figure 2. The generated particles randomly.](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Localization_particle_filter/Graphs/Fig2.png)  

### Measurements
In practice, the distance between the robot and landmarks can be measured by the sensors. Here, assumed that the position of the robot is (x, y) and the position of the first landmark is (x0, y0), the distance can be calculated by the following equation:  
![Equation 1](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Localization_particle_filter/Graphs/Eq1.png)
In the above equation, “e” is the error generated by noises, which is often represented by a random number. In other words, the robot can only get the estimation of distance nearby the exact value.  

### Importance weight
According to Equation (1), the estimated distance between each particle and each landmark can be calculated. It can be concluded that the particles with large distance are less likely to be the exact position, while the particles with short distance are more likely to be the exact position. In this step, the importance weight of each particle is imported to determine this probability. The importance weight can be computed by Equation (2).  
![Equation 2](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Localization_particle_filter/Graphs/Eq2.png)
Here, 2 denotes the variance of the measurement noise. x is the sum of the measurements between particle and four landmarks. The calculation of  is similar to that of x, while the error in Equation (1) is different, hence the value of x and  are also different. Once the importance weight is determined, we can get to know the belief of each particle.  

### Resample
Ideally, we can select the particles with high weights to represent the distribution of the actual position. However, the problem of particle degeneracy may emerge after several iterations, that is only the particles with highest weights will be retained while other particles will be removed. As a result, the diversity of the particles decreases.  
In this step, the purpose is to select the particles with high importance weight, meanwhile don’t destroy the diversity of the particles. The methods are varied, such as multinomial resampling[2], stratified resampling[3], residual resampling[4] and systematic resampling[5]. In this project, a tricky solution called resampling wheel is applied.  
I learned this method in the lesson of autonomous vehicles on Udacity and it is pretty funny and innovative. As shown in Figure 3, the resampling wheel is composed by all of the particles and each particle occupied a slice that corresponds to its importance weight. Particles with a bigger weight occupy more space, whereas particles with a smaller weight occupy less space. 
Initially, the index of particle is generated randomly, like w5. Then, we select a random value  which is positive and no more than 2 times of the maximal weight. If the value of  is larger than w5, the 5-th particle will be selected. Otherwise, the value of  is updated to ( – w5). Then we set the index to 6 and compare the value of w6 and  to determine whether the 6-th particle should be selected. Repeating this process until N new particles are selected. Of course, a particle could appear several times in the new particles set. But the problem of particles degeneracy could be avoided since the value of  is random as a result some particles with small weights can also be retained.  
The process of resampling wheel can be expressed directly by the following sentences:  
![Resample](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Localization_particle_filter/Graphs/resample.png)
![Figure 3. Diagram of resampling wheel](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Localization_particle_filter/Graphs/Fig3.png)

## Results analysis
The process of particle filter is implemented by Python. In this section, the localization accuracy will be evaluated under different parameters, like the number of particles and variance of noises. Here, I will calculate the means of x and y values of all the retained particles as the estimated value, and compute the error of the estimated value.  

### Errors under different number of particles
General speaking, more particles means higher accuracy since there are more particles located nearby the exact position. However, too many particles will increase the computation and affect the localization speed. Here, I set the number of particles to 500, 1000 and 3000 respectively and record their localization errors in Table 1.  
The results suggest that the localization error will increase when the number of particles are too many or less. When the number of particles is set to 1000, the localization accuracy is most satisfying.   
![Table1](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Localization_particle_filter/Graphs/Table1.png)

### Errors after iterations
In reality, the mobile robot moves continually to complete specific tasks, as a result the position of robot is changing constantly. It is crucial to guarantee the localization accuracy even after many iterations. Here, I set the yaw angle and distance manually to change the position of robot and then measure the distance between robot and four landmarks to update the position of robot. A good algorithm must be robust enough to converge to the exact position after iterations. The results are shown in Figure 4.  
![Figure 4. The errors of x and y](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Localization_particle_filter/Graphs/Fig4.png)  
Obviously, the localization errors will decrease as the iterations increase, thanks to more knowledge of position is obtained. Figure 5 displays the relative position of particles after four iterations more intuitively.  
![Figure 5. Particles after iterations.](https://github.com/Key1994/Course_of_self-driving_car_Udacity/blob/master/Localization_particle_filter/Graphs/Fig5.png)  

## Conclusion
In this article, I build a model to simulate the typical robot localization task. Then, the particle filter algorithm is applied to locate mobile robot from a scratch, and get a satisfying result eventually. The results reveal that particle filter has a strong robustness to work against environmental uncertainty, thus is an efficient technique to locate mobile robot globally.  
However, the implementation of particle filter indicates that the problem of particles degeneracy is likely to occur if the resampling method was not applied, which will decrease the performance of particle filter. In addition, the number of particles affects the final localization accuracy and efficiency.  

## References
> [1]	D. Fox, Markov localization for mobile robots in dynamic environments. 1999.  
> [2]	N. J. Gordon, D. J. Salmond, and A. F. M. Smith, "Novel Approach to Nonlinear/Non-Gaussian Bayesian State Estimation," Radar and Signal Processing, IEE Proceedings F, vol. 140, pp. 107-113, 05/01 1993, doi: 10.1049/ip-f-2.1993.0015.  
> [3]	J. Carpenter, P. Clifford, and P. Fearnhead, "Improved particle filter for nonlinear problems," IEE Proceedings - Radar, Sonar and Navigation, vol. 146, no. 1, pp. 2-7, 1999, doi: 10.1049/ip-rsn:19990255.  
> [4]	J. S. Liu and R. Chen, "Sequential Monte Carlo Methods for Dynamic Systems," Publications of the American Statistical Association, vol. 93, no. 443, pp. 1032-1044.  
> [5]	A. Doucet, "On sequential Monte Carlo methods for Bayesian filtering," Statistics & Computing, vol. 10, no. 3, pp. 197-208, 1998.  



