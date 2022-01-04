from glob import glob
import json
from collections import Counter
import shutil
from pathlib import Path
import numpy as np

"""
检查数据，
1、检查图片和标注文件是否一一对应，如果没有，返回该图片名称，或标注文件
2、判断json文件里是否有有标注信息，如果没有，返回该json文件，并删除，
3、如果标注信息的imagePath错误，则按照图片名称改正
"""

base_path = Path('/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/jingpinfeigang_cc')
print('base_path is', base_path)


# base_chaochang = Path('/Users/clustar/Desktop/项目/金盛兰数据_料件/超长件')

# base_path = '/Users/clustar/Desktop/项目/金盛兰数据_料件'


def GetAllImage():
    date_list = glob(f'{base_path}/*')
    date_set = [date.split('/')[-1] for date in date_list]
    date_set = sorted(date_set)
    date_final = []
    for date_ in date_set:
        if date_.isdigit():
            date_final.append(date_)
    image_list = []
    for date_id in date_final:
        file_list = glob(f'{base_path}/{date_id}/*/*')
        file_list = sorted(file_list)
        for image_ in file_list:
            if image_.endswith('jpg'):
                image_list.append(image_)
    return image_list


def GetAllJson():
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
    return json_list


def ImgAndJsonMatch():
    image_list = GetAllImage()
    # print(image_list)
    errorimg_list = []
    for img in image_list:
        jsonflie = img.replace('.jpg', '.json')
        if not Path(jsonflie).exists():
            errorimg_list.append(img)
            Path(img).unlink()
    print(errorimg_list)
    print(len(errorimg_list))
    print("无标注文件的图片删除成功")


def JsonisNUll():
    json_list = GetAllJson()
    # print(json_list)
    # print(len(json_list))
    errorjson_list = []
    for js in json_list:
        with open(js, 'r+', encoding='utf8') as fp:
            check_data = json.load(fp)
            if "shapes" not in check_data:
                errorjson_list.append(js)
            else:
                if len(check_data['shapes']) == 0:
                    errorjson_list.append(js)
                    img = js.replace('.json', '.jpg')
                    Path(img).unlink()
                    Path(js).unlink()
                else:
                    imgPath = check_data['imagePath']
                    jpgname = Path(js).name.replace('.json', '.jpg')
                    if not str(imgPath) == str(jpgname):
                         check_data['imagePath'] = jpgname
                    fp.seek(0)  # rewind
                    json.dump(check_data, fp, ensure_ascii=False)
                    fp.truncate()
    print(errorjson_list)
    print(len(errorjson_list))
    print("无标注信息的样本删除成功,错误图像名称修改成功")


def Testjsoninforisright():
    json_list = GetAllJson()
    errorjson = []
    for i in json_list:
        with open(i, 'r+', encoding='utf8') as fp:
            check_data = json.load(fp)
            imgPath = check_data['imagePath']
            jpgname = Path(i).name.replace('.json', '.jpg')
            if not str(imgPath) == str(jpgname):
                errorjson.append(i)
                print("错误文件为：", i)
    if len(errorjson) == 0:
        print("标注文件均正确")

if __name__ == '__main__':
    # ImgAndJsonMatch()
    # JsonisNUll()
    alljson = GetAllJson()
    allimage = GetAllImage()
    if len(alljson) == len(allimage):
        print("图像和标注文件匹配")
    else:
        print("图像和标注文件不匹配")
    Testjsoninforisright()

