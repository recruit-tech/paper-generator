# -*- coding: utf-8 -*-
import struct
from PIL import Image, ImageOps, ImageEnhance
import os

target_name = 'ETL9G'

for root, dirs, files in os.walk(target_name):
    for i, file in enumerate(sorted(files)):
        filepath = os.path.join(root, file)
        print(file)
        
        sum_datasets = 4
        sum_words = 3036
        record_size = 8199
        
        with open(filepath, 'rb') as f:
            for ds_idx in range(0, sum_datasets * sum_words):
                f.seek(ds_idx * record_size)
                s = f.read(record_size)
                r = struct.unpack('>2H8sI4B4H2B34x8128s7x', s)

                iF = Image.frombytes('F', (128, 127), r[14], 'bit', 4)
                iP = iF.convert('L')
                enhancer = ImageEnhance.Brightness(iP)
                iE = enhancer.enhance(20)
                img = ImageOps.invert(iE)

                file_name = '{}_{}_{}_{}_{}_{}.png'.format(target_name, i, r[0], hex(r[1])[2:], r[3], ds_idx)
                dir_name = "./{}_img/{}".format(target_name, hex(r[1])[2:])

                os.makedirs(dir_name, exist_ok=True)
                img.save(os.path.join(dir_name, file_name), 'PNG')
