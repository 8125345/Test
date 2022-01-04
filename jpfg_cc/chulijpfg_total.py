#-*- coding: UTF-8 -*-
from glob import glob
import json
from collections import Counter
import shutil
from pathlib import Path
import numpy as np


base_path = Path('/Users/clustar/Desktop/项目/金盛兰数据_超长/多料件')
print('base_path is', base_path)
base_chaochang = Path('/Users/clustar/Desktop/项目/金盛兰数据_超长/多料件测试')
base_chaochang.mkdir(parents=True, exist_ok=True)


def GetAllJson(base_path1):
    base_path1 = base_path
    date_list = glob(f'{base_path1}/*')
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
    return json_list


def StatisticHavechaochangJson():
    lab_list = []
    have_chaochang_json = []
    json_list = GetAllJson(base_path)
    for i in json_list:
        with open(i, 'r', encoding='utf8') as fp:
            check_data = json.load(fp)
            for item in check_data['shapes']:
                lab_list.append(item['label'])
                if str(item['label']) == 'jpfg_cc':
                    have_chaochang_json.append(i)
    have_chaochang_json = np.unique(have_chaochang_json)
    have_chaochang_json_list = list(have_chaochang_json)
    print('有精品废钢超长件的图片数量是：', len(have_chaochang_json_list))
    return have_chaochang_json

def Copyfile2newfile():
    date_new_list = []
    car_num_new_list = []
    date_car_list = []
    have_chaochang_json_list = StatisticHavechaochangJson()
    for have_chaochang_json_l in have_chaochang_json_list:
        date_car = str(have_chaochang_json_l).split('/')[-3:-1]  ##日期+车次
        date_car_list.append(date_car)
    date_car_dict = {}
    for date_car_ in date_car_list:
        date_new_list.append(date_car_[0])
        car_num_new_list.append(date_car_[1])
    date_new_list = np.unique(date_new_list)
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

def delete_duoliaojian():
    json_list = GetAllJson(base_chaochang)
    for i in json_list:
        with open(i, 'r+', encoding='utf8') as fp:
            check_data = json.load(fp)
            check_data_list = check_data['shapes']
            # print(check_data_list)
            # print(check_data_list)
            for i, item in enumerate(check_data_list):
                if not str(item['label']).endswith('_cc'):
                    item.clear()
            # print(check_data_list)
            fp.seek(0)  # rewind
            json.dump(check_data, fp, ensure_ascii=False)
            fp.truncate()
    print("删除多料件完成")

def deletenulldict():
    json_list = GetAllJson(base_chaochang)
    for i in json_list:
        with open(i, 'r+', encoding='utf8') as fp:
            check_data = json.load(fp)
            check_data_list = check_data['shapes']
            for i in range(len(check_data_list) - 1, -1, -1):
                if check_data_list[i] == {}:
                    check_data_list.pop(i)
            fp.seek(0)  # rewind
            json.dump(check_data, fp, ensure_ascii=False)
            fp.truncate()
    print("删除空字典完成")



if __name__ == '__main__':
    Copyfile2newfile()
    delete_duoliaojian()
    deletenulldict()

