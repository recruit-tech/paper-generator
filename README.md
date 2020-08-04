# Paper generator
Utilities for ATL paper ocr prj


## **adjust_rotation**
### USAGE
cd adjust_rotation  
python image_adjust_rotate.py  out_sample_m_c_r1_01.jpeg -5 5

### OUTPUT
This script rotates the document image to find the best angle b/w -5 to 5 degrees with 0.5 steps.

## **create_companies_name**
### USAGE
cd create_companies_name  
./create_company_names.sh  

### Output
The above script will generate a fictitious company name and output it as standard out.   
Here are fictitious company.  
清水製作所橋本商事株式会社  
合資会社アクロスオーシャン  
株式会社山本工業中央商事  
有限会社サカイハピネス  
中島製作所大翔株式会社  
有限会社グリーンイシダ  
グロース大和合資会社  
エフテックリンクス株式会社  
アライブパートナー株式会社


## **create_field_images**

### USAGE
cd create_field_images  
python create_image_from_text.py アライブパートナー株式会社 /home/y/.local/share/fonts/azuki.ttf 200 60

### OUTPUT
The script finds a font size that fits exactly in the width and height you specify.  
In above case, text is "アライブパートナー株式会社", font is azkuki.ttf, width is 200, height is 60.  

## **image_augmentation**

### USAGE
cd image_augmentation  
python image_augmentation.py input_pdf output_pdf

### OUTPUT
Ths script reads pdf files in input_pdf directory and outputs augmented files which are applied some noise. 


  
## **pdf2jpeg**

### USEGE(pdf to images)
cd pdf2jpeg
python pdf2jpeg.py pdf/out_sample_b.pdf  

### OUTPUT(pdf to images)
This command converts 1 pdf file to image files  

### USEGE(images to pdf)
cd pdf2jpeg
python pdf2jpeg.py output/out_sample_m_c_r1_01.jpeg output/out_sample_m_c_r1_02.jpeg output/out_sample_m_c_r1_03.jpeg

### OUTPUT(images to pdf)
This command converts 3 images to pdf file.



