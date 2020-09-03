function weights = generate_weights(n)
weights = [];
w0 = (1-n)/1;
weights(1) = w0;
for i = 2:(2*n+1)
    weights(i) = 1/(2*1);
end 
end