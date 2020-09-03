function sigma_point =  generate_point(x_o, n, P)
    sigma_point = [];
    sigma_point(:,1) = x_o;
    A = chol(1*P);
    for i = 2:(n+1)
        sigma_point(:,i) = x_o + A(:,i-1);
    end
    for i = (n+2) : (2*n+1)
        sigma_point(:,i) = x_o -A(:,i-n-1);
    end
end
