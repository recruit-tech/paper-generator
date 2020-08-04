# -*- coding: utf-8 -*-
import os
import pathlib
from pathlib import Path
from pdf2image import convert_from_path
import sys
import cv2
import numpy as np
import img2pdf
from PIL import Image

# poppler/binを環境変数PATHに追加する
poppler_dir = Path(__file__).parent.absolute() / "poppler/bin"
os.environ["PATH"] += os.pathsep + str(poppler_dir)

def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image

def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ""
    return answer

def pdf2jpeg(pdf_path,dpi=200):
    pages = convert_from_path(str(pdf_path), dpi)
    images = []
    for img in pages:
        images.append(pil2cv(img))

    return images

def images2pdf(image_pathes,outputfile):
    with open(outputfile, "wb") as f:
        f.write(img2pdf.convert([i for i in image_pathes] ))

    return

def saveImagesAsPDF(images,outputfile):
    img_list = []
    cnt = 0 
    for img in images:
        if cnt == 0:
            im1 = cv2pil(img).convert('RGB') 
        else:
            img_list.append(cv2pil(img).convert('RGB'))
        cnt += 1

    im1.save(outputfile,save_all=True, append_images=img_list)




if __name__ == '__main__':
    args = sys.argv
    if len(args) < 1:
        print("python pdf2jpeg.py xxx.pdf")
        print("or")
        print("python pdf2jpeg.py aaa.jpeg bbb.jpeg ccc.jpeg ...")
        exit()
    elif len(args) == 2:
        pdf_path = args[1]
        pages = pdf2jpeg(pdf_path)

        image_dir = Path("output")
        for i, page in enumerate(pages):
            file_name = pathlib.Path(pdf_path).stem + "_{:02d}".format(i + 1) + ".jpeg"
            image_path = image_dir / file_name
            print(image_path)
            # JPEGで保存
            cv2pil(page).save(str(image_path), "JPEG")

        #for i, page in enumerate(pages):
        #    print(type(numpy.array(page)))
        #    cv2.imshow("page",numpy.array(page))
        #    cv2.waitKey(0)

    else:
        image_pathes = []
        for i in range(1,len(args)):
            image_pathes.append(args[i])
        outputfile = longestSubstringFinder(image_pathes[0], image_pathes[1]) + '.pdf'
        images2pdf(image_pathes,outputfile)
