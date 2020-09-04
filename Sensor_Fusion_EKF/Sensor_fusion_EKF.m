clc;
clear;

dt = 0.1;    % Sampling time
% Load data
data = csvread('Users/zhangzheng/Desktop/Lidar-and-Radar-sensor-fusion-with-Extended-Kalman-Filter-master/Radar_Lidar_Data1.csv',1,1);
Radar_Measurement = [];
Lidar_Measurement = [];
E_Lidar = [];
E_Radar = [];
EKF_Path = [];
EKF_velocity = [];
radar_velocity = [];

% System matrix
A = [1, 0, dt, 0; 0, 1, 0, dt;  0, 0, 1, 0; 0, 0, 0, 1];
B = [0.5*dt^2, 0; 0, 0.5*dt^2; dt, 0; 0, dt];
% Observation matrix
C = [1, 0, 0, 0; 0, 1, 0, 0];
u = 0;
% Initial state vector
X = [data(1,6:7), 0, 0]' ;

% Initial covariance matrix of estimated error
P = [[1, 0, 0, 0];
     [0, 1, 0, 0];
     [0, 0, 100, 0];
     [0, 0, 0, 100]];
 % Covariance matrix of Lidar measurement
R_l = [[0.0025, 0];
       [0, 0.0025]];
% Covariance matrix of Radar measurement
R_r = [[0.0025, 0, 0];
      [0, 0.0025, 0];
      [0, 0, 0.0025]];
  % Covariance matrix of process noise
  Q = [(dt^2)/4, 0, (dt^3)/2, 0;
     0, (dt^2)/4, 0, (dt^3)/2;
     (dt^3/2), 0, (dt^2), 0;
     0, (dt^3)/2, 0, (dt^2)];

for n = 1:length(data)
    % Prior estimation
        X = A * X + B * u;
        P = A * P * A' + Q;
     
    % State update via Lidar measurement    
    if data(n, 1) == 1
        z = data(n, 2:3)';
        K = P * C' * inv(C * P *C' +R_l);
        X = X + K * (z - C *X);
        P = (eye(4) - K * C) * P;
       EKF_Path = [EKF_Path;[X(1),X(2)]];    % Estimation result of EKF
       E_Lidar = [E_Lidar; data(n, 2:3) - data(n, 6:7)]; %Measurement error of Lidar
    
    % State update via Radar measurement
    else
         z = data(n, 2:4)';
         x = X(1); y = X(2); vx = X(3); vy = X(4);
         c1 = x^2 + y^2;
         c2 = sqrt(c1);
         c3 = c1^(3/2);
         
         if c1 == 0
             J = [0, 0, 0, 0; 0, 0, 0, 0; 0, 0, 0, 0];
         else
            J = [x/c2, y/c2, 0, 0; -y/c1, x/c1, 0, 0; vx/c2-x*(x*vx+y*vy)/c3, vy/c2-y*(x*vx+y*vy)/c3, x/c2, y/c2];   % Jacobian matrix
         end
        
         K = P * J' * inv(J * P * J' + R_r);
         y = [c2; atan(y/x); (x * vx + y * vy)/c2];
         X = X + K * (z - y);
         P = (eye(4) - K*J)*P;
         EKF_Path = [EKF_Path;[X(1),X(2)]]; % Estimation result of EKF
         rho = data(n, 2);
         phi = data(n, 3);
         rho_dif = data(n, 4);
         radar_velocity = [radar_velocity; [rho_dif*cos(phi)-data(n,8), rho_dif*sin(phi)-data(n,9)]]; % Velocity measurement of Radar
         EKF_velocity = [EKF_velocity; [X(3) - data(n, 8), X(4)-data(n,9)]];   % Velocity estimation via EKF
         E_Radar = [E_Radar; [rho*cos(phi), rho*sin(phi)] - data(n, 6:7)];%Measurement error of Radar
        
    end
end

E_EKF= EKF_Path - data(:,6:7);    % Estimation error of EKF (Position)
MAE_EKF = mean(abs(E_EKF));   % MAE of EKF  (Position)
RMSE_EKF = sqrt((sum(E_EKF).^2)/n);   % RMSE of EKF (Position)

MAE_Lidar = mean(abs(E_Lidar));    %  MAE of Lidar
RMSE_Lidar = sqrt((sum(E_Lidar).^2)/n*2);    %RMSE of Lidar

MAE_Radar = mean(abs(E_Radar));     %  MAE of Radar (Position)
RMSE_Radar = sqrt((sum(E_Radar).^2)/n*2);  %  RMSE of Radar  (Position)

E_velocity = EKF_velocity - radar_velocity;   % Estimation error of EKF  (Velocity)
MAE_velocity_r = mean(abs(radar_velocity));   % MAE of Radar (Velocity)
MAE_velocity_E = mean(abs(EKF_velocity));  % MAE of EKF (Velocity)
RMSE_Radar_velocity = sqrt((sum(radar_velocity).^2)/n*2);  %  RMSE of Radar (Velocity)
RMSE_EKF_velocity = sqrt((sum(EKF_velocity).^2)/n*2);    %  RMSE of EKF (Velocity)

figure;
plot(data(:,6),data(:,7), 'linewidth', 2);
hold on;
scatter(EKF_Path(:,1),EKF_Path(:,2),10,'filled','r');
legend('Groundtruth', 'EKF');
xlabel('X'); ylabel('Y');
title('Result')
hold off;

figure;
plot(E_EKF, 'green');
title('Error');

        