# coding:utf-8

import pathlib
import sys
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../create_field_images' )
sys.path.append( str(current_dir) + '/../ETL_tools' )

import xml.etree.ElementTree as ET


import argparse    
import sys
import glob, os
import numpy as np
import cv2
import xml.etree.ElementTree as ET
from lxml import etree
import pandas as pd
import random
import create_image_from_text

from PIL import Image
import text2etlimg

import csv
def rotateImage(img, angle):
    center_x = int(img.shape[1]/2)
    center_y = int(img.shape[0]/2)
    img_PIL=Image.fromarray(~img )
    img_PIL=img_PIL.rotate(angle , center=(center_x, center_y) )
    output_img = np.asarray(img_PIL)
    return ~output_img

def getCharacterRect(charcter_img):
    black_pixels_mask = np.all(charcter_img == [0, 0, 0], axis=-1)
    vertical_histgram = np.where(black_pixels_mask.sum(axis=1))

    #All pixel are white
    if len(vertical_histgram[0]) == 0:
        return -1,-1,-1,-1

    y_min = vertical_histgram[0][0]
    y_max = vertical_histgram[0][len(vertical_histgram[0])-1]
    calc_height = y_max + y_min
    #print ("y_min:",y_min,"y_max",y_max,"hight",calc_height)

    horizontal_histgram = np.where(black_pixels_mask.sum(axis=0))
    x_min = horizontal_histgram[0][0]
    x_max = horizontal_histgram[0][len(horizontal_histgram[0])-1]
    calc_width = x_max + x_min
    #print ("x_min:",x_min,"x_max",x_max,"width",calc_width)

    return x_min,y_min,x_max,y_max

def getCroppedImage(img):
    crop_margin_x = 15
    crop_margin_y = 3
    white = ~np.zeros(img.shape, np.uint8)
    #white[0:img.shape[0]-1,int((img.shape[1]-1)*(crop_margin_x/100)):int((img.shape[1]-1)*((100-crop_margin_x)/100))] = img[0:img.shape[0]-1,int((img.shape[1]-1)*(crop_margin_x/100)):int((img.shape[1]-1)*((100-crop_margin_x)/100))] 
    y_min = int((img.shape[0]-1)*(crop_margin_y/100))
    y_max = int((img.shape[0]-1)*((100-crop_margin_y)/100))
    x_min = int((img.shape[1]-1)*(crop_margin_x/100))
    x_max = int((img.shape[1]-1)*((100-crop_margin_x)/100))
    white[y_min:y_max,x_min:x_max] = img[y_min:y_max,x_min:x_max]
    
    return white
    

def getThresholdImage(src):
    #if cv2.countNonZero(src)==0:
    #    return src

    h = src.shape[0]
    w = src.shape[1]
    _, img = cv2.threshold(src, 190, 255, cv2.THRESH_BINARY)
    rate = 1.0 - (cv2.countNonZero(img)/(w*h))

    if rate < 0.5:
        return img

    #cv2.imshow('src',img)

    pre_contours_len = 0
    start_flg = False
    for thresh in range(0,250,10):
        _, img = cv2.threshold(src, thresh, 255, cv2.THRESH_BINARY)
        rate = 1.0 - (cv2.countNonZero(img)/(w*h))
        contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print('thresh',thresh)
        #print('rate',rate)
        #print('len(contours)',len(contours))

        if start_flg:
           if pre_contours_len < len(contours):
               break

        if pre_contours_len > len(contours):
            start_flg = True

        pre_contours_len = len(contours)
        pre_thresh = thresh
        #cv2.imshow('img',img)
        #cv2.waitKey(0)
        


    _, img = cv2.threshold(src, pre_thresh, 255, cv2.THRESH_BINARY)
    #cv2.imshow('best',img)
    #cv2.waitKey(0)

    return img


def getTextImage(text):
    imgs = text2etlimg.getETLImages(text)
    angles = np.arange(-5.0, 5.0, 0.5)
    margins = range(0,20,1)
    max_height = max([img.shape[0] for img in imgs])
    max_width = max([img.shape[1] for img in imgs])


    resized_imgs = []
    for img in imgs:
        img = getCroppedImage(img)
        img = getThresholdImage(img)
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB) 
        height = img.shape[0]
        width = img.shape[1]
        angle = np.random.choice(angles)
        img = rotateImage(img,angle)
        #if max_width != width or max_height != height:
        #    img = cv2.resize(img, (max_width, max_height))
        x_min,y_min,x_max,y_max = getCharacterRect(img)
        if x_min < 0:
            continue
        w = x_max - x_min
        h = y_max - y_min

        if w <= 0 or h <= 0:
            continue

        center_x = int(w/2) + x_min
        center_y = int(h/2) + y_min

        if w > h:
            y_min = max(center_y - int(w/2),0)
            y_max = min(center_y + int(w/2),height)
        #else:
        #    x_min = max(center_x - int(h/2),0)
        #    x_max = min(center_x + int(h/2),width)

        resized_imgs.append( img[y_min:y_max,x_min:x_max] )
        #textImage[0:y_max, x_offset:x_offset+(x_max-x_min)] |= ~img[0:y_max,x_min:x_max]
        #x_offset += (x_max-x_min)
        #x_offset += np.random.choice(margins)
    #print('len',len(resized_imgs))
    if len(resized_imgs)==0:
        #for i in imgs:
        #    cv2.imshow('i',i)
        #    cv2.waitKey(0)
        return False,imgs[0]

    max_height = max([img.shape[0] for img in resized_imgs])
    max_width = max([img.shape[1] for img in resized_imgs])
    total_width = sum([img.shape[1] for img in resized_imgs])
    #print('total_width',total_width)
    #print('max(margins)',max(margins))
    #print('len(resized_imgs)',len(resized_imgs))
    #print('max_width',max_width)
    textImage = np.zeros((max_height, int((max_width + max(margins)) * len(resized_imgs) * 2), 3), np.uint8)
    #print('textImage',textImage.shape)
    x_offset = 0
    for img in resized_imgs:
        height = img.shape[0]
        width = img.shape[1]
        #if max_width != width or max_height != height:
        if max_height != height:
            img = cv2.resize(img, (int(width*(max_height/height)), max_height))
        #print('img.shape',img.shape)
        #print('max_height',max_height)
        #print('x_offset',x_offset)
        #cv2.imshow('img',img)
        #cv2.imshow('textImage',textImage)
        #cv2.waitKey(0)
        
        textImage[0:max_height, x_offset:x_offset+img.shape[1]] |= ~img
        x_offset += img.shape[1]
        x_offset += np.random.choice(margins)

    return True, ~textImage[0:-1, 0:x_offset]


def getTestImageList(text):
    imgs = []
    imgs.append(cv2.imread('./src_imgs/ETL9B_21_2422_3037.png'))
    imgs.append(cv2.imread('./src_imgs/ETL9B_21_2424_3038.png'))
    imgs.append(cv2.imread('./src_imgs/ETL9B_21_2426_3039.png'))
    imgs.append(cv2.imread('./src_imgs/ETL9B_22_2428_3040.png'))
    imgs.append(cv2.imread('./src_imgs/ETL9B_22_242a_3041.png'))
    return imgs

def convert_count_by_country(csv_data):
    data = {}
    for date, country, confirmed ,deaths, recovered in zip(csv_data['ObservationDate'], csv_data['Country/Region'],csv_data['Confirmed'],csv_data['Deaths'],csv_data['Recovered']):
        date = re.sub("[0-9]{2}:[0-9]{2}:[0-9]{2}","",date)
        if len(date) == 8:
            date = re.sub(r'(^[0-9]{2}/[0-9]{2}/)[0-9]{2}$',r'\1',date) + re.sub(r'^[0-9]{2}/[0-9]{2}/([0-9]{2}$)',r'20\1',date)

        if country not in data:
            data.setdefault(country,{date:[0, 0, 0]})

        if date not in data[country]:
            data[country].setdefault(date, [0, 0, 0])

        data[country][date][0] += float(confirmed)
        data[country][date][1] += float(deaths)
        data[country][date][2] += float(recovered)

    return data

def read_csv(filename):
    data = {}
    with open(filename,encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            for cnt, name in enumerate(header):
                if name not in data:
                    data[name] = []
                data[name].append(row[cnt])
    return data

def getRandomText(in_csvs, db_name, idx):
    filename = os.path.join(in_csvs, db_name + ".csv")
    df = pd.read_csv(filename)
    text = random.choice(df.values.tolist())
    #print(text)

    return text

def putTextImageOnPage(base, img, x_offset, y_offset, width, height):

    #cv2.imshow('src',cv2.resize(src,(int(src.shape[1]*0.5),int(src.shape[1]*0.5))))

    if width < img.shape[1]:
        img = cv2.resize(img, (width, int(img.shape[0]*(width/img.shape[1]))))

    if height < img.shape[0]:
        img = cv2.resize(img, (int(img.shape[1]*(height/img.shape[0])),height ))

    base[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] |= ~img
    #dst = ~src | base
    #cv2.imshow('dst',cv2.resize(base,(int(base.shape[1]*0.5),int(base.shape[1]*0.5))))
    #cv2.waitKey(0)
    return base

def process4xml(in_imgs_dir, filepath, out_imgs_dir, in_csvs):
    if not os.path.exists(out_imgs_dir):
        os.makedirs(out_imgs_dir)

    file = open(filepath)
    tree = ET.parse(file)
    root = tree.getroot()

    objs = []

    folder = root.find('folder').text
    filename = root.find('filename').text
    path = root.find('path').text
    source = root.find('source')
    database = source.find('database').text
    size = root.find('size')
    width = size.find('width').text
    height = size.find('height').text
    depth = size.find('depth').text
    segmented = root.find('segmented').text

    filename, ext = os.path.splitext(os.path.basename(filepath))
    print("filename",filename)
    #image_file_path = filename + '.jpeg'
    image_file_path = os.path.join("./" + in_imgs_dir , filename + '.jpeg')
    if os.path.isfile(image_file_path) == False:
        image_file_path = os.path.join("./" + in_imgs_dir , filename + '.png')

    page_img = cv2.imread(image_file_path)

    #text = random.choice(df.values.tolist())
    #print(os.path.join("./" + in_csvs , filename))
    data = read_csv(os.path.join("./" + in_csvs , filename + '.csv'))
    #print('data[]',data)
    #exit()

    cnt=0
    data_exist = True
    while data_exist:
        src = page_img.copy()
        base = np.zeros(src.shape,dtype=np.uint8)
        output_image_file_path = os.path.join("./" + out_imgs_dir , filename + '-' + str(cnt).zfill(4) + '.png')
        print(output_image_file_path)
        for obj in root.iter('object'):
            name = obj.find('name').text
            bndbox = obj.find('bndbox')
            b = [int(bndbox.find('xmin').text), int(bndbox.find('ymin').text), int(bndbox.find('xmax').text), int(bndbox.find('ymax').text)]
            width = int(bndbox.find('xmax').text) - int(bndbox.find('xmin').text)
            height = int(bndbox.find('ymax').text) - int(bndbox.find('ymin').text)

            objs.append([name] + b )
            db_name = objs[0]

            x_offset = int(bndbox.find('xmin').text)
            y_offset = int(bndbox.find('ymin').text) 
            #text = getRandomText(in_csvs, filename,i)
            if cnt > len(data[name])-1:
                data_exist = False
                print(cnt)
                break
            #print('cnt',cnt)
            #print('len(data[name])',len(data[name]))
            #print( data[name][cnt])
            text = data[name][cnt]
            print(name,':',text)
            if len(text) == 0:
                print('continie')
                continue
            #text_img = create_image_from_text.create_image_from_text(str(text[0]), font, width, height)
            #print(str(text)) 
            ret, text_img = getTextImage(str(text))
            if ret == False:
                print('brea')
                break
            #cv2.imwrite("sample-" + name + '_' + str(cnt).zfill(4) + '.png',text_img)

            base = putTextImageOnPage(base, text_img, x_offset, y_offset, width, height)

            #img = cv2.resize(text_img, (int(width*(max_height/height)), max_height))
        
            #img[y_offset:y_offset+text_img.shape[0], x_offset:x_offset+text_img.shape[1]] = text_img
            #dst = ~src | img

        cnt += 1
        dst = ~(~src | base)

        #cv2.imshow('dst',cv2.resize(dst,(int(dst.shape[1]*0.5),int(dst.shape[1]*0.5))))
        #cv2.waitKey(0)
        cv2.imwrite(output_image_file_path,dst)
    #filename, ext = os.path.splitext(os.path.basename(filepath))




def get_arguments():
    parser = argparse.ArgumentParser(description='isnkavsnkanl')
    parser.add_argument('in_imgs_dir',help='Specify images directory')   
    parser.add_argument('in_xmls_dir', help='Specify XML directory')   
    parser.add_argument('in_csvs_dir', help='Specify csv directory')   
    parser.add_argument('--out_imgs_dir',default='results/imgs')   
    args = parser.parse_args()

    print('args.in_imgs_dir :'+args.in_imgs_dir)
    print('args.in_xmls_dir :'+args.in_xmls_dir)
    print('args.in_csvs_dir :'+args.in_csvs_dir)
    print('args.out_imgs_dir :'+args.out_imgs_dir)
    return args.in_imgs_dir, args.in_xmls_dir, args.in_csvs_dir, args.out_imgs_dir

if __name__ == '__main__':
    in_imgs, in_xmls, in_csvs, out_imgs  = get_arguments()

    for f in os.listdir(in_xmls):
        if f.endswith(".xml"):
            process4xml(in_imgs, os.path.join( "./" + in_xmls  + "", f), out_imgs, in_csvs )

