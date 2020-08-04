# -*- coding: utf-8 -*-
import sys
import pandas as pd
import random
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def pil2cv(imgPIL):
    imgCV_RGB = np.array(imgPIL, dtype = np.uint8)
    imgCV_BGR = np.array(imgPIL)[:, :, ::-1]
    return imgCV_BGR

def cv2pil(imgCV):
    imgCV_RGB = imgCV[:, :, ::-1]
    imgPIL = Image.fromarray(imgCV_RGB)
    return imgPIL

def cv2_putText_1(img, text, org, fontFace, fontScale, color):
    x, y = org
    b, g, r = color
    colorRGB = (r, g, b)
    imgPIL = cv2pil(img)
    draw = ImageDraw.Draw(imgPIL)
    fontPIL = ImageFont.truetype(font = fontFace, size = fontScale)
    draw.text(xy = (x,y), text = text, fill = colorRGB, font = fontPIL)
    imgCV = pil2cv(imgPIL)
    return imgCV

def fontSizeAdjustRect(text, font, width, height, min_fontsize=1, max_fontsize=100):
    x, y = 0, 0
    fontScale = 1
    thickness = 1
    colorBGR = (0,0,0)
    #size = 10

    for size in range(max_fontsize,min_fontsize,-1):
        test = np.full((height*2,width*2,3), (255,255,255), dtype=np.uint8)
        test = cv2_putText_1(img = test,
                             text = text,
                             org = (x,y),
                             fontFace = font,
                             fontScale = size,
                             color = colorBGR)

        black_pixels_mask = np.all(test == [0, 0, 0], axis=-1)
        vertical_histgram = np.where(black_pixels_mask.sum(axis=1))
        #print('vertical_histgram',vertical_histgram[0])
        y_min = vertical_histgram[0][0]
        y_max = vertical_histgram[0][len(vertical_histgram[0])-1]
        #calc_height = y_max - y_min
        calc_height = y_max + y_min
        #print ("y_min:",y_min,"y_max",y_max,"hight",calc_height)

        horizontal_histgram = np.where(black_pixels_mask.sum(axis=0))
        #print('horizontal_histgram',horizontal_histgram)
        x_min = horizontal_histgram[0][0]
        x_max = horizontal_histgram[0][len(horizontal_histgram[0])-1]
        #calc_width = x_max - x_min
        calc_width = x_max + x_min
        #print ("x_min:",x_min,"x_max",x_max,"width",calc_width)

        
        if width >= calc_width and height >= calc_height:
            #cv2.imshow('test',test)
            #cv2.waitKey(0)
            break;


    print ("size",size,"width",calc_width,"hight",calc_height)
    return size, calc_width, calc_height

def create_image_from_text(text, font, width, height):
    size, calc_width, calc_height = fontSizeAdjustRect(text, font, width, height)
    img = np.full((height,width,3), (0,0,0), dtype=np.uint8)

    x = 0
    y = int((height - calc_height)/2)
    fontScale = 1
    thickness = 1
    colorBGR = (255,255,255)
    img = cv2_putText_1(img = img,
                        text = text,
                        org = (x,y),
                        fontFace = font,
                        fontScale = size,
                        color = colorBGR)
    return   img




if __name__ == '__main__':
    args = sys.argv
    text = args[1]
    fontPIL = args[2]
    print(fontPIL)
    width = int(args[3])
    height = int(args[4])

    img = create_image_from_text(text, fontPIL, width, height)
    cv2.imshow('result',img)
    cv2.waitKey(0)

