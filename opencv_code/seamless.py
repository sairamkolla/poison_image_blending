# Written by sairam kolla on Nov 26th 2015
# All rights reserved

#imports

import cv2
import numpy as np
from scipy.sparse import lil_matrix,csr_matrix
from scipy.sparse.linalg import spsolve
def construct_polygon(event,x,y,flags,points):
    if event == cv2.EVENT_LBUTTONDOWN:
        print y, " " , x
        points.append((x,y))
    return
if __name__ == "__main__":
    background_img = cv2.imread('nabla_f.png')
    border_img = cv2.imread('wall.jpg')
    border_img = border_img.astype(np.float)
    m,n = len(background_img),len(background_img[0])
    points = []
    cv2.imshow('get_input',background_img)
    cv2.setMouseCallback('get_input',construct_polygon,points)
    cv2.waitKey(0)
    cv2.destroyWindow('get_input')


    '''Create mask from the input image'''
    mask = np.zeros((m,n),np.uint8)
    cv2.fillPoly(mask, np.array([points]), (255,255,255))
    ret, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
    cv2.imshow('mask', mask)
    cv2.waitKey(0)
    cv2.destroyWindow('mask')
    ''' Find length of the coeff matrix'''
    nz_pixels = np.nonzero(mask)
    num_pixels = len(nz_pixels[0])
    print "num of white pixels - ", num_pixels
    indices = np.zeros((m,n),np.uint32)
    count = 0
    for i in range(0,num_pixels):
        y = nz_pixels[0][i]
        x = nz_pixels[1][i]
        indices[y, x] = count
        count += 1
    ''' Calculate the laplacian at each point'''

    grad_img = np.zeros((m, n, 3),np.float)
    background_img = background_img.astype(np.float)
    H = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]],np.float)
    grad_img = cv2.filter2D(background_img, -1, H)


    print "Laplacians calculated"
    '''max of 5 pixels'''
    Coeff_matr = lil_matrix((num_pixels,num_pixels))        # this matrix has 4*num_pixels vales at maximum
    #Coeff_matr = csr_matrix((num_pixels,num_pixels))        # this matrix has 4*num_pixels vales at maximum
    #Coeff_matr = np.zeros((num_pixels,num_pixels))        # this matrix has 4*num_pixels vales at maximum
    B = np.zeros((num_pixels, 3),np.float)

    ''' iterate over every pixel in the image'''
    print "size of image is ",m, "  ",n
    for y in range(1,m-2+1):
        for x in range(1,n-2+1):
            ''' only add points that are in the mask'''
            if mask[y,x] == 255:
                neighbours = 1
                '''take care of neighbours'''
                '''top boundary'''
                if mask[y - 1, x] == 1:
                    Coeff_matr[indices[y, x], indices[y - 1, x]] = -1
                    neighbours += 1
                else:
                    for chnl in range(0,3):
                        B[indices[y, x], chnl] = B[indices[y, x], chnl] +  (border_img[y - 1, x, chnl])
                        print indices[y,x],"  ",border_img[y - 1, x, chnl]
                '''left boundary'''
                if mask[y, x - 1] == 1:
                    Coeff_matr[indices[y, x], indices[y, x - 1]] = -1
                    neighbours += 1
                else:
                    for chnl in range(0,3):
                        B[indices[y, x], chnl] = B[indices[y, x], chnl] +  (border_img[y, x - 1, chnl])
                        print indices[y, x], "  ", border_img[y , x-1, chnl]
                ''' bottom boundary '''
                if mask[y + 1, x] == 1:
                    Coeff_matr[indices[y, x], indices[y + 1, x]] = -1
                    neighbours += 1
                else:
                    for chnl in range(0,3):
                        B[indices[y, x], chnl] = B[indices[y, x], chnl] +  (border_img[y + 1, x, chnl])
                        print indices[y, x], "  ", border_img[y + 1, x, chnl]
                ''' right boundary '''
                if mask[y, x + 1] == 1:
                    Coeff_matr[indices[y, x], indices[y, x + 1]] = -1
                    neighbours += 1
                else:
                    for chnl in range(0,3):
                        B[indices[y, x], chnl] = B[indices[y, x], chnl] +  (border_img[y, x + 1, chnl])
                        print indices[y, x], "  ", border_img[y, x + 1, chnl]
                for chnl in range(0,3):
                    B[indices[y, x], chnl] = B[indices[y, x], chnl] + grad_img[y, x, chnl]
                Coeff_matr[indices[y, x], indices[y, x]] = 4

    final_img = border_img.astype(np.float)
    ''' solving Ax = B'''

    Coeff_matr = Coeff_matr.tocsr()
    #print len(Coeff_matr.nonzero()[0])
    solns = spsolve(Coeff_matr,B)
    #solns = solve(Coeff_matr,B)
    #print solns
    for k  in range(0,num_pixels):
        y = nz_pixels[0][k]
        x = nz_pixels[1][k]
        for ch in range(0,3):
            final_img[y,x,ch] = solns[k,ch]
        #final_img[y, x, :] = solns[k,:]

    final_img = final_img.astype(np.uint8)

    cv2.imshow('final',final_img)
    cv2.waitKey(0)
    cv2.destroyWindow('final')

'''
b,g,r = cv2.split(img)
img2 = cv2.merge([r,g,b])
plt.imshow(img2) # expect true color
plt.show()
'''