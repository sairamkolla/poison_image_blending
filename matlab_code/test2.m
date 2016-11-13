img1 = imread('water_back.jpeg'); 
[H,W,C] = size(img1);
img =  imread('water_front.png');
img = double(img);
% Find gradinets
% Reconstruct image from gradients for verification
img_rec = zeros(H,W,3);
for num=1:3
    gx = zeros(H,W); 
    gy = zeros(H,W); 
    j = 1:H-1; k = 1:W-1;
    gx(j,k) = (img(j,k+1,num) - img(j,k,num));
    gy(j,k) = (img(j+1,k,num) - img(j,k,num));
    
%     gx(j,k) = max(gx(j,k),img1(j,k+1,num) - img1(j,k,num));
%     gy(j,k) = max(gy(j,k),img1(j+1,k,num) - img1(j,k,num));
    img_rec(:,:,num) = poisson_solver_function(gx,gy,img1(:,:,num));
end
figure,imshow(uint8(img-img_rec));
figure,imshow(uint8(img_rec));
figure,imshow(uint8(img));