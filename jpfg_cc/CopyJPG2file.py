#-*- coding: UTF-8 -*-
from glob import glob
import json
import os
from pathlib import Path
import shutil

"""
将图片拷贝到一个文件夹里
"""

base_dir = '/Users/clustar/Desktop/项目/车牌识别/1号车位车牌/'


# labelme_json = glob(os.path.join(base_dir, "*.json"))
# print(labelme_json)


date_list = glob(f'{base_dir}/*')
date_set = [date.split('/')[-1] for date in date_list]
date_set = sorted(date_set)
date_final = []
for date_ in date_set:
    if date_.isdigit():
       date_final.append(date_)


jpg_list = []
for date_id in date_final:
    file_list = glob(f'{base_dir}/{date_id}/*')
    file_list = sorted(file_list)
    for jpg_ in file_list:
        if jpg_.endswith('jpg'):
            jpg_list.append(jpg_)

print(len(jpg_list))
image_dir = Path('/Users/clustar/Desktop/项目/车牌识别/一号车位图片汇总')
image_dir.mkdir(parents=True, exist_ok=True)

if image_dir.exists():
    for img in jpg_list:
        shutil.copy2(img, image_dir)
else:
    print('路径不存在')


#
#
# lab_list = []
# for i in json_list:
#     with open(i, 'r+', encoding='utf8') as fp:
#          check_data = json.load(fp)
#          check_data_list = check_data['shapes']
#          # print(check_data_list)
#          # print(check_data_list)
#          for i, item in enumerate(check_data_list):
#              lab_list.append(item['label'])
#              if not str(item['label']) == 'jpfg_cc':
#                  item.clear()
#
#          # print(check_data_list)
#          fp.seek(0)  # rewind
#          json.dump(check_data, fp, ensure_ascii=False)
#          fp.truncate()