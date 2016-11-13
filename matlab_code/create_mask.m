function BW = create_mask(I)
img = imread(I);
h_im = imshow(img);
h = imfreehand;
position = wait(h);
BW = createMask(h,h_im);
