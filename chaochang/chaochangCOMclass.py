from pathlib import Path
from glob import glob
import json

base_dir = Path('/Users/clustar/Desktop/项目/金盛兰数据_超长/chaochang_only的副本')

date_list = glob(f'{base_dir}/*')
date_set = [date.split('/')[-1] for date in date_list]
date_set = sorted(date_set)
date_final = []
for date_ in date_set:
    if date_.isdigit():
       date_final.append(date_)


json_list = []
for date_id in date_final:
    file_list = glob(f'{base_dir}/{date_id}/*/*')
    file_list = sorted(file_list)
    for json_ in file_list:
        if json_.endswith('json'):
            json_list.append(json_)

lab_list = []

for i in json_list:
    with open(i, 'r+', encoding='utf8') as fp:
         check_data = json.load(fp)
         check_data_list = check_data['shapes']
         # print(check_data_list)
         # print(check_data_list)
         for i, item in enumerate(check_data_list):
             lab_list.append(item['label'])
             if str(item['label']).endswith('_cc'):
                 item['label'] = 'cc'
         # print(check_data_list)
         fp.seek(0)  # rewind
         json.dump(check_data, fp, ensure_ascii=False)
         fp.truncate()