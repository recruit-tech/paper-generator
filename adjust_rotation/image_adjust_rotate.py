# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sys



def rotate(img, angle):
    rows,cols = img.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
    return dst

def sum_rows(img):
    # Create a list to store the row sums
    row_sums = []
    # Iterate through the rows
    for r in range(img.shape[0]-1):
        # Sum the row
        row_sum = sum(sum(img[r:r+1,:]))
        # Add the sum to the list
        row_sums.append(row_sum)
    # Normalize range to (0,255)
    row_sums = (row_sums/max(row_sums)) * 255
    # Return
    return row_sums


def adjustAngle(image, start_angle=-5,end_angle=5):
    #src = 255 - cv2.imread(image_path,0)
    src = 255 - image
    h,w = src.shape
    small_dimention = min(h,w)
    src = src[:small_dimention, :small_dimention]

    # Rotate the image around in a circle
    min_score = 99999999
    best_angle = 0
    angle = start_angle
    while angle <= end_angle:
        # Rotate the source image
        img = rotate(src, angle)    
        # Crop the center 1/3rd of the image (roi is filled with text)
        h,w = img.shape
        buffer = min(h, w) - int(min(h,w)/1.5)
        #roi = img.copy()
        roi = img[int(h/2-buffer):int(h/2+buffer), int(w/2-buffer):int(w/2+buffer)]
        # Create background to draw transform on
        bg = np.zeros((buffer*2, buffer*2), np.uint8)
        # Threshold image
        _, roi = cv2.threshold(roi, 140, 255, cv2.THRESH_BINARY)
        # Compute the sums of the rows
        row_sums = sum_rows(roi)
        # High score --> Zebra stripes
        score = np.count_nonzero(row_sums)
        #print('angle',angle,'score',score)
        if score < min_score:
            min_score = score
            best_angle = angle
        angle += .5
    return best_angle
    

if __name__ == '__main__':
    args = sys.argv
    image_path = args[1]

    angle = 0
    image = cv2.imread(image_path,0)
    if len(args) > 2:
        start_angle = int(args[2])
        end_angle = int(args[3])

        if start_angle > end_angle:
            tmp_angle = end_angle
            end_angle = start_angle
            start_angle = tmp_angle
  
        angle = adjustAngle(image,start_angle,end_angle)
    else:
        angle = adjustAngle(image)


    print('The best angle',angle)
    rotated_img = rotate(image, angle)    
    cv2.imshow('rotated_img',rotated_img)
    cv2.waitKey(0)
