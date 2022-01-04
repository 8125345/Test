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


base_path = Path('/Users/clustar/Desktop/项目/金盛兰数据_超长/chaochang_only')
print('base_path is', base_path)
base_chaochang = Path('/Users/clustar/Desktop/项目/金盛兰数据_超长/chaochang_except_jpfgcc')
base_chaochang.mkdir(parents=True, exist_ok=True)
# base_path = '/Users/clustar/Desktop/项目/金盛兰数据_料件'

date_list = glob(f'{base_path}/*')
date_set = [date.split('/')[-1] for date in date_list]
date_set = sorted(date_set)
date_final = []
for date_ in date_set:
    if date_.isdigit():
       date_final.append(date_)
# print(date_final)

json_list = []
for date_id in date_final:
    file_list = glob(f'{base_path}/{date_id}/*/*')
    file_list = sorted(file_list)
    for json_ in file_list:
        if json_.endswith('json'):
            json_list.append(json_)

# print(len(json_list))
# error_name= ['jyfg','ZZ','PF','zf2_yw','jqfg','zf1cc','jpfgcc','gyfy']

# f = open('/Users/clustar/Desktop/项目/金盛兰数据')
have_chaochang_json = []
for i in json_list:
    lab_list = []
    with open(i, 'r', encoding='utf8') as fp:
         check_data = json.load(fp)
         for item in check_data['shapes']:
             lab_list.append(item['label'])
             # if str(item['label']) == 'jpfg_cc':
             #除去含有精品废钢超长的料件
         if 'jpfg_cc' not in lab_list:
             for item in check_data['shapes']:
                 if str(item['label']).endswith('cc'):
                     have_chaochang_json.append(i)
             # if item['label'] in error_name:
# print(len(lab_list))
# for w_c_j in with_chaochang_json:
#     print(w_c_j)
have_chaochang_json = np.unique(have_chaochang_json)
# print(have_chaochang_json)
# print(type(list(have_chaochang_json)))
have_chaochang_json_list = list(have_chaochang_json)
print('有精品废钢超长件的图片数量是：', len(have_chaochang_json_list))
date_new_list = []
car_num_new_list = []
date_car_list =[]
for have_chaochang_json_l in have_chaochang_json_list:
    date_car = str(have_chaochang_json_l).split('/')[-3:-1]  ##日期+车次
    date_car_list.append(date_car)

# print(date_car_list)
date_car_dict = {}
for date_car_ in date_car_list:
    date_new_list.append(date_car_[0])
    car_num_new_list.append(date_car_[1])
date_new_list = np.unique(date_new_list)
# car_num_new_list = np.unique(car_num_new_list)
# print(date_new_list)
# print(car_num_new_list)

for date_new_ in date_new_list:
    temp = []
    for date_car_ in date_car_list:
        if date_new_ == date_car_[0]:
            temp.append(date_car_[1])
        else:
            continue
    temp = np.unique(temp)
    # print(temp)
    date_car_dict[date_new_] = list(temp)
# print(date_car_dict)

for DATE_CAR in date_car_dict:
    # print(DATE_CAR)
    DATE_DIR = base_chaochang / f'{DATE_CAR}'
    DATE_DIR.mkdir(parents=True, exist_ok=True)
    for CAR in date_car_dict[DATE_CAR]:
        CAR_DIR = base_chaochang / f'{DATE_CAR}' / f'{CAR}'
        CAR_DIR.mkdir(parents=True, exist_ok=True)

for have_chaochang_json_l in have_chaochang_json_list:
    # print(have_chaochang_json_l)
    have_chaochang_image = str(have_chaochang_json_l).replace('.json', '.jpg')
    date__ = str(have_chaochang_json_l).split('/')[-3]
    car__ = str(have_chaochang_json_l).split('/')[-2]
    dst_dir = base_chaochang / f'{date__}' / f'{car__}'
    if dst_dir.exists():
        shutil.copy2(have_chaochang_json_l, dst_dir)
        shutil.copy2(have_chaochang_image, dst_dir)
    else:
        print('路径不存在')











# print(lab_list)
# my_label = set(lab_list)
# print(my_label)

# for i in my_label:
#     if str(i).endswith('_cc'):
#         print("%s:%d" % (i, lab_list.count(i)))








