clc;
clear;
format short;

data = csvread('Users/zhangzheng/Desktop/Sensor_Fusion_UKF/Radar_Lidar_Data1.csv',1,1);

% X = [x, y, v, s, sd];
X = [data(2,2:3), 1, 0.1, 0]';

new_sig = [];
P = [[0.01,0,0,0,0,];
            [0,0.01,0,0,0];
            [0,0,0.01,0,0];
            [0,0,0,0.01,0];
            [0,0,0,0,0.01]];
Q= [0.0009,0;0,0.0009];
          
Rr = [0.09,0,0;0,0.05,0;0,0,0.09];
Rl = [0.09, 0; 0, 0.09];
np = 7;
nm = 5;
T = 0.05;
UKF = [];
 
%  for k =1:length(data)
for k=1: 400
     X_aug = [X; 0.8; 0.8];
     for i=1:nm
        P_aug(i,:) = [P(i,:), 0,0];
     end
     P_aug(6,:) = [0,0,0,0,0,Q(1,:)];
     P_aug(7,:) = [0,0,0,0,0,Q(2,:)];
     A = chol(2*P_aug);
     sigma_point = generate_point(X_aug, np, P_aug);
     for i = 1:(2*np+1)
         Xa = sigma_point(:,i);
         x = Xa(1); y = Xa(2); v = Xa(3); s = Xa(4); sd = Xa(5); mu_a = Xa(6); mu_s = Xa(7);
         if sd <=0.5
             x=x+v*cos(s)*T+T^2*mu_a*cos(s)/2;
             y=y+v*sin(s)*T+T^2*mu_a*sin(s)/2;
             v=v+mu_a*T;
             s=s+ T^2*mu_s/2;
             sd = sd +mu_s*T;
             new_sig(:,i) =[x, y, v, s, sd]';
         else
             x = x + v*(sin(s+sd*T)-sin(s))/sd + T^2*mu_a*cos(s)/2;
             y = y + v*(sin(s)- cos(s+sd*T))/sd + T^2*mu_a*sin(s)/2;
             v = v + mu_a*T;
             s = s + sd*T + T^2*mu_s/2;
             sd = sd +mu_s*T;
             new_sig(:,i) =[x, y, v, s, sd]';
         end
     end

     weights = generate_weights(np);
     mx = new_sig*weights';
     P = zeros(nm);
     for i = 1:15
    	 sig_xe(:,i) = new_sig(:,i) - mx;
         P = P + weights(i)*sig_xe(:,i)*sig_xe(:,i)';
     end

     if data(k,1) == 1
         z_sig = zeros(2,15);
         sig_ze = zeros(2,15);
         Tk = zeros(5,2);
         z = data(k,2:3);
         H = [1,0,0,0,0; 0,1,0,0,0];
         z_sig = H*new_sig;
         mz = z_sig*weights';
         S = zeros(2);
        for i = 1:15
            sig_ze(:,i) = z_sig(:,i) - mz;
            S = S + weights(i)*sig_ze(:,i)*sig_ze(:,i)';
        end
        S = S+Rl;
        for i =1:15
            tk = weights(i)*sig_xe(:,i)*sig_ze(:,i)';
            Tk = Tk+tk;
        end
        K = Tk*inv(S);
        X = X+K*(z' - mz);
        P = P+K*S*K';
        
        
%      else
%          z = data(k,2:4);
%          z_sig = zeros(3,15);
%          sig_ze = zeros(3,15);
%          for i =1:15
%             z_sigpt = new_sig(:,i);
%             x = z_sigpt(1); y = z_sigpt(2); v = z_sigpt(3); s = z_sigpt(4); sd = z_sigpt(5);
%             rho = sqrt(x^2+y^2);
%             phi = atan(y/x);
% %             rho_dif = (v*cos(s)*x+v*sin(s)*y)/sqrt(x^2+y^2);
%             rho_dif = (v*x+v*y)/sqrt(x^2+y^2);
%             z_sig(:,i) = [rho, phi, rho_dif];
%          end
%          mz = z_sig*weights';
%          S = zeros(3);
%         for i = 1:15
%             sig_ze(:,i) = z_sig(:,i) - mz;
%             S = S + weights(i)*sig_ze(:,i)*sig_ze(:,i)';
%         end
%         S = S+Rr;
%         Tk = zeros(5,3);
%         for i =1:15
%             tk = weights(i)*sig_xe(:,i)*sig_ze(:,i)';
%             Tk = Tk+tk;
%         end
%         K = Tk*inv(S);
%         Xr = X+K*(z' - mz);
%         X(1) = Xr(1)*cos(Xr(2));
%         X(2) = Xr(1)*sin(Xr(2));
%         X(3) = X(3);
%         X(4) = X(4);
%         X(5) = X(5);
%         P = P+K*S*K';
%         UKF = [UKF;X(1:2)'];   
     end

     UKF = [UKF;X(1:2)'];   

     
 end
 
 E = [];
 for i =2:length(UKF)
     if data(i,1) == 1
        e = UKF(i,:)-data(i,6:7);
     else
         e = UKF(i,:)-data(i-1,6:7);
     end
 E = [E;e];
 end
 ave = mean(abs(E));
            

