# -*- coding: utf-8 -*-
import struct
from PIL import Image, ImageOps
import os

target_name = 'ETL9B'

for root, dirs, files in os.walk(target_name):
    for i, file in enumerate(sorted(files)):
        filepath = os.path.join(root, file)
        print(file)
        
        sum_datasets = 40
        sum_words = 3036
        record_size = 576
        
        with open(filepath, 'rb') as f:
            for ds_idx in range(1, sum_datasets * sum_words + 1):
                f.seek(ds_idx * record_size)
                s = f.read(record_size)
                r = struct.unpack('>2H4s504s64x', s)
                i1 = Image.frombytes('1', (64, 63), r[3], 'raw')
                img = ImageOps.invert(i1.convert('L'))

                file_name = '{}_{}_{}_{}_{}.png'.format(target_name, i, r[0], hex(r[1])[2:], ds_idx)
                dir_name = "./{}_img/{}".format(target_name, hex(r[1])[2:])

                os.makedirs(dir_name, exist_ok=True)
                img.save(os.path.join(dir_name, file_name), 'PNG')
