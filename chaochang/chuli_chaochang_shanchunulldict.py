from glob import glob
import json
from collections import Counter
import shutil
from pathlib import Path
import numpy as np

'''
删除空字典，最后要执行这个程序
'''


base_path = Path('/Users/clustar/Desktop/项目/金盛兰数据_超长/chaochang_except_jpfgcc')
# print('base_path is', base_path)
# base_chaochang = Path('/Users/clustar/Desktop/项目/金盛兰数据_料件/超长件')

# base_path = '/Users/clustar/Desktop/项目/金盛兰数据_料件'

date_list = glob(f'{base_path}/*')
date_set = [date.split('/')[-1] for date in date_list]
date_set = sorted(date_set)
date_final = []
for date_ in date_set:
    if date_.isdigit():
       date_final.append(date_)


json_list = []
for date_id in date_final:
    file_list = glob(f'{base_path}/{date_id}/*/*')
    file_list = sorted(file_list)
    for json_ in file_list:
        if json_.endswith('json'):
            json_list.append(json_)


lab_list = []
# have_chaochang_json = []
# for i in json_list:
#     with open(i, 'r', encoding='utf8') as fp:
#          check_data = json.load(fp)
#          for item in check_data['shapes']:
#              lab_list.append(item['label'])

# print(len(lab_list))
# # print(lab_list)
# my_label = set(lab_list)
# # print(my_label)
# for i in my_label:
#     if str(i).endswith('_cc'):
#         print("%s:%d" % (i, lab_list.count(i)))



#####删除除超长外的其他标注

# for i in json_list:
#     with open(i, 'r+', encoding='utf8') as fp:
#          check_data = json.load(fp)
#          check_data_list = check_data['shapes']
#          # print(check_data_list)
#          print(check_data_list)
#          for item in check_data_list:
#              print()
         # for i, item in enumerate(check_data_list):
         #     lab_list.append(item['label'])
             # if not str(item['label']).endswith('_cc'):
             #     item.clear()

         # print(check_data_list)
         # fp.seek(0)  # rewind
         # json.dump(check_data, fp, ensure_ascii=False)
         # fp.truncate()

###删除json里的空{}
for i in json_list:
    with open(i, 'r+', encoding='utf8') as fp:
         check_data = json.load(fp)
         check_data_list = check_data['shapes']
         for i in range(len(check_data_list)-1, -1, -1):
             if check_data_list[i] == {}:
                check_data_list.pop(i)
         fp.seek(0)  # rewind
         json.dump(check_data, fp, ensure_ascii=False)
         fp.truncate()





# str1 = '/Users/clustar/Desktop/项目/金盛兰数据_料件/chaochang的副本/20210608/EAUH652/EAUH652_2_20210608115351.json'
# with open(str1, 'r+', encoding='utf8') as fp:
#     check_data = json.load(fp)
#     check_data_list = check_data['shapes']
#     print(check_data_list)
#     for i in range(len(check_data_list)-1, -1, -1):
#         if check_data_list[i] == {}:
#             check_data_list.pop(i)
#     print(check_data_list)










