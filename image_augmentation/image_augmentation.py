# -*- coding: utf-8 -*-
import random
from scipy.stats import norm
from numpy.random import *
import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import os
from os import path
from os import listdir
from os.path import isfile, join
import pathlib
import sys
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../pdf2jpeg' )
#from pdf2jpeg import pdf2jpeg
import pdf2jpeg 
import time

from PIL import Image
def apply_solt_pepper(image,noise):
      row,col,ch = image.shape
      s_vs_p = 0.5
      amount = noise
      out = np.copy(image)
      # Salt mode
      #print(image.shape)
      num_salt = np.ceil(amount * image.size * s_vs_p)
      coords = [np.random.randint(0, i - 1, int(num_salt))
              for i in image.shape[:2]]
      out[tuple(coords)] = (255,255,255)

      # Pepper mode
      num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
      coords = [np.random.randint(0, i - 1, int(num_pepper))
              for i in image.shape[:2]]
      out[tuple(coords)] = (0,0,0)
      return out


def blur_noise(image,noise):
    #noise = min(max(1,int(normal(1 ,10))),10)
    return cv2.blur(image,(noise,noise))

def line_noise(image):
    row,col,ch = image.shape
    #cv2.imshow('src',image)

    max_line_appearance_rate = 5
    coords = np.random.choice([i for i in range(0,row-1)],int( (np.random.randint(1,max_line_appearance_rate)*row)/100), replace=False)

    image[coords,:,:] = 255
    return image


def cnvBGR2BGRA(image_bgr):

    h, w, c = image_bgr.shape
    # append Alpha channel -- required for BGRA (Blue, Green, Red, Alpha)
    image_bgra = np.concatenate([image_bgr, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
    # create a mask where white pixels ([255, 255, 255]) are True
    white = np.all(image_bgr == [255, 255, 255], axis=-1)
    # change the values of Alpha to 0 for all the white pixels
    image_bgra[white, -1] = 0
    # save the image
    return image_bgra



def applyNoise(pdf,blur,solt_pepper):

    dpis = [150,200,300]
    dpi = np.random.choice(dpis)
    images = pdf2jpeg.pdf2jpeg(pdf,dpi)

    #print(mpl.get_configdir() + '/matplotlibrc')
    #print(mpl.rcParams['backend'])

    #blur = min(max(1,int(normal(1 ,5))),5)
    #solt_pepper = normal(0.004 ,0.0005)

    output_images = []

    for img in images:

        output  = cnvBGR2BGRA(img.copy())
        output = apply_solt_pepper(img,solt_pepper) 
        output = line_noise(output)
        output = blur_noise(output,blur)
        w, h = output.shape[:2]
        
        center_x = np.random.randint(int(w*3/10), int((w-1)*7/10))
        center_y = np.random.randint(int(h*3/10), int((h-1)*7/10)) 
        output_PIL=Image.fromarray(output )

        angles = [-2.0,-1.5,0,1.5,2.0]
        angle = np.random.choice(angles)
        output_PIL=output_PIL.rotate(angle , center=(center_x, center_y) )

        output = np.asarray(output_PIL)
        
        output_images.append(output)

    return output_images

if __name__ == '__main__':

    args = sys.argv

    pdf_input_path = args[1]
    pdf_output_path = args[2]
    os.makedirs(pdf_output_path, exist_ok=True)

    pdffiles = sorted([f for f in listdir(pdf_input_path) if isfile(join(pdf_input_path, f))])
    cnt = 0
    for pdf in pdffiles:
        print(pdf)
        for blur in [1,3]:
            for solt_pepper in [0.002,0.004]:
               images = applyNoise(path.join(pdf_input_path , pdf), blur, solt_pepper)
               output_filename = pdf_output_path + '/' + os.path.splitext( pdf)[0] + 'blur_' + str(blur) +  '_s&p_' + str(solt_pepper) +  '.pdf'
               #print(output_filename)
               pdf2jpeg.saveImagesAsPDF(images,output_filename)
