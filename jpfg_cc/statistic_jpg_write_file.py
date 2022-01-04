#-*- coding: UTF-8 -*-
from glob import glob
import json
from collections import Counter
import shutil
from pathlib import Path
import numpy as np

'''
统计精品废钢超长写入文件
统计所有数据集里超长件的mask数量，并且将含有超长件的图片重新复制到新文件夹中，
'''


base_path = Path('/home/zhaoliang/mmdetection/data/alldata/')
print('base_path is', base_path)
base_jpg = Path('/home/zhaoliang/mmdetection/data/alldata/image')
base_jpg.mkdir(parents=True, exist_ok=True)
# base_path = '/Users/clustar/Desktop/项目/金盛兰数据_料件'

date_list = glob(f'{base_path}/*')
date_set = [date.split('/')[-1] for date in date_list]
date_set = sorted(date_set)
date_final = []
for date_ in date_set:
    if date_.isdigit():
       date_final.append(date_)
# print(date_final)

image_list = []
for date_id in date_final:
    file_list = glob(f'{base_path}/{date_id}/*/*')
    file_list = sorted(file_list)
    for image_ in file_list:
        if image_.endswith('jpg'):
            image_list.append(image_)


for img in image_list:
    if base_jpg.exists():
        shutil.copy2(img, base_jpg)
    else:
        print('路径不存在')











# print(lab_list)
# my_label = set(lab_list)
# print(my_label)

# for i in my_label:
#     if str(i).endswith('_cc'):
#         print("%s:%d" % (i, lab_list.count(i)))








