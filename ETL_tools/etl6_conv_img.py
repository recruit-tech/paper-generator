# -*- coding: utf-8 -*-
import struct
from PIL import Image, ImageOps, ImageEnhance
import os

target_name = 'ETL6'

for root, dirs, files in os.walk(target_name):
    for i, file in enumerate(sorted(files)):
        filepath = os.path.join(root, file)
        print(file)
        
        sum_datasets = 1383 * 10
        record_size = 2052
        
        with open(filepath, 'rb') as f:
            for ds_idx in range(0, sum_datasets):
                f.seek(ds_idx * record_size)
                s = f.read(record_size)
                r = struct.unpack('>H2sH6BI4H4B4x2016s4x', s)

                iF = Image.frombytes('F', (64, 63), r[18], 'bit', 4)
                iP = iF.convert('L')
                enhancer = ImageEnhance.Brightness(iP)
                iE = enhancer.enhance(10)
                img = ImageOps.invert(iE)

                file_name = '{}_{}_{}_{}_{}_{}.png'.format(target_name, i, r[0], hex(r[3])[2:], r[9], ds_idx)
                dir_name = "./{}_img/{}".format(target_name, hex(r[3])[2:])
                    
                os.makedirs(dir_name, exist_ok=True)
                img.save(os.path.join(dir_name, file_name), 'PNG')
