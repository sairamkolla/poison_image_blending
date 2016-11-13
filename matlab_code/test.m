clear all;
close all;
img_back = imread('wall.jpg');
img = imread('nabla_f.png');
%% polycrop input image

f1 = figure;
imshow(img);
[BW,xi,yi] = roipoly;
close(f1);
x = regionprops(BW,'BoundingBox');
i1 = imcrop(img,x(1).BoundingBox);
BW = imcrop(BW,x(1).BoundingBox);
i1 = i1.*repmat(uint8(BW),[1,1,3]);
%% Polycrop target image

f1 = figure;
imshow(img_back);
h = impoly(gca, [xi yi]);
setVerticesDraggable(h,0);
api = iptgetapi(h);
fcn = makeConstrainToRectFcn('impoly',[1 size(img_back,1)],[1 size(img_back,2)]);
api.setPositionConstraintFcn(fcn);
new_poly = wait(h);
close(f1);

BW_main = poly2mask(new_poly(:,1),new_poly(:,2), size(img_back,1),size(img_back,2));
x = regionprops(BW_main,'BoundingBox');
i2 = imcrop(img_back,x(1).BoundingBox);
BW = imcrop(BW_main,x(1).BoundingBox);
i2 = i2.*repmat(uint8(BW),[1,1,3]);
%% Verify sizes of both images
if size(i1,1) > size(i2,1)
    i1 = i1(1:size(i2,1),:,:);
elseif size(i1,1) < size(i2,1)
    i2 = i2(1:size(i1,1),:,:);
end
if size(i1,2) > size(i2,2)
    i1 = i1(:,1:size(i2,2),:);
elseif size(i1,2) < size(i2,2)
    i2 = i2(:,1:size(i1,2),:);
end

%%  Explicitly for rectangle!! ( Not required, polygon is the new fashion)

% %%code for selection of required rect
% S = [1 1 size(img,2)-1 size(img,1)-1];
% I = img_back; % your input image
% figure, imshow(I);
% h = imrect(gca, S);
% addNewPositionCallback(h,@(p) title(mat2str(p,3)));
% fcn = makeConstrainToRectFcn('imrect',get(gca,'XLim'),get(gca,'YLim'));
% setPositionConstraintFcn(h,fcn)
% position = wait(h);
% I2 = imcrop(I,position);
% imshow(I2);   % the output image of your ROI
% img1 = I2;

%% Actual Code
% img(1:136,1:142,:) = img2;
[H,W,C] = size(i1);
i2 = double(i2);
img_rec = zeros(H,W,3);
for num=1:3
    gx = zeros(H,W); 
    gy = zeros(H,W); 
    j = 1:H-1; k = 1:W-1;
    gx(j,k) = (i1(j,k+1,num) - i1(j,k,num));
    gy(j,k) = (i1(j+1,k,num) - i1(j,k,num));
    
    gx(j,k) = max(gx(j,k),i2(j,k+1,num) - i2(j,k,num));
    gy(j,k) = max(gy(j,k),i2(j+1,k,num) - i2(j,k,num));
    img_rec(:,:,num) = poisson_solver_function(gx,gy,i2(:,:,num));
end
%img_back(position(1):position(1)+size(img,1)-1,position(2):position(2)+size(i1,2)-1,:) = uint8(img_rec);
% temp = zeros([size(BW_main) 3]);
% temp(x(1).BoundingBox,:) = img_rec;
% img_back(:,:,1) = BW_main.*img_back(:,:,1) + (~BW_main).*img_rec;
% 
% figure,imshow(img_back);
figure
imshowpair(i1,i2,'montage');
figure
imshow(img_rec);
