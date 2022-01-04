from pathlib import Path
from glob import glob
import shutil
from collections import Counter
import json
import cv2
import math
import numpy as np


def integer(x):
    return math.ceil(x)


def get_labels(json_path):
    null_json_list = []
    if Path(json_path).exists():
        # totallist = []
        with open(json_path, 'r+', encoding='utf8') as fp:
            check_data = json.load(fp)
            if 'shapes' in check_data:
                check_data_list = check_data['shapes']
                for data in check_data_list:
                    # dict1 = dict()
                    plate = str(data['label']).replace('_', '')
                    corner = data['points']
                    # totallist.append(dict1)
                # print(totallist)
                return plate, corner
            else:
                null_json_list.append(json_path)
    else:
        print('标注文件不存在')


def batchjson2txt(json_file, txt_dir):
    with open(txt_dir, 'w+') as f:
        for jso in json_file:
            if jso.endswith('.json'):
                # print(Path(xml).parent.name)
                plate_label = get_labels(jso)
                if plate_label is not None:
                    f.writelines(f'img/{Path(jso).stem}.jpg' + '\t' + str(plate_label) + '\n')


def GetAllJson(dir):
    date_list = glob(f'{dir}/*')
    date_set = [date.split('/')[-1] for date in date_list]
    date_set = sorted(date_set)
    date_final = []
    for date_ in date_set:
        if date_.isdigit():
            date_final.append(date_)
    json_list = []
    for date_id in date_final:
        file_list = glob(f'{dir}/{date_id}/*')
        file_list = sorted(file_list)
        for json_ in file_list:
            if json_.endswith('json'):
                json_list.append(json_)
    return json_list


def crop_image_from_json(dir):
    json_list = GetAllJson(dir)
    for js in json_list:
        _, point = get_labels(js)
        img_dir = js.replace('json', 'jpg')
        img = cv2.imread(img_dir)
        cropped = img[0:128, 0:512]  # 裁剪坐标为[y0:y1, x0:x1]
        cv2.imwrite("./data/cut/cv_cut_thor.jpg", cropped)


def crop_image_test():
    img = cv2.imread(
        '/Users/clustar/Desktop/项目/车牌识别/一号车位车牌数据/1号车位车牌原始数据/20211207/chegnshi_1cp_20211207033252_5795366.jpg')
    ori_im = np.copy(img)
    # points = np.array([[893.5263157894736, 329.47368421052636],
    #          [1077.7368421052631, 426.8421052631579],
    #          [1080.3684210526317, 497.8947368421052],
    #          [893.5263157894736, 403.1578947368421]])
    #
    # img_crop_width = int(
    #     max(
    #         np.linalg.norm(points[0] - points[1]),
    #         np.linalg.norm(points[2] - points[3])))
    # img_crop_height = int(
    #     max(
    #         np.linalg.norm(points[0] - points[3]),
    #         np.linalg.norm(points[1] - points[2])))
    #
    # print(points[0] - points[1])
    # print(np.linalg.norm(points[0] - points[1]))
    # print(np.linalg.norm(points[2] - points[3]))

    """
        [
          893.5263157894736,
          329.47368421052636
        ],   左上（x0,y0）
        [
          1077.7368421052631,
          426.8421052631579
        ],   右上
        [
          1080.3684210526317,
          497.8947368421052
        ],   右下（x1,y1）
        [
          893.5263157894736,
          403.1578947368421
        ]   左下
    """
    left_top = [866, 330]
    right_bottom = [1107, 500]

    crop = ori_im[330:500, 866:1107]  # 裁剪坐标为[y0:y1, x0:x1]
    # cv2.imwrite("/Users/clustar/Desktop/项目/车牌识别/crop_text/", crop)

    # print(math.ceil(329.47368421052636))
    cv2.imshow("result1", crop)
    cv2.imshow("result", img)
    cv2.waitKey(0)


def generate_croplabel_from_txt(base_dir, save_dir):
    txt_dir = f'{base_dir}/test.txt'
    save_txt = f'{save_dir}/test.txt'
    with open(txt_dir, 'r') as f:
        with open(save_txt,'w') as f_s:
            lines = f.readlines()
            # print(len(lines))
            # print(lines)
            for line in lines:
                img_name = line.split('\t')[0].replace('img', 'crop')
                label = eval(line.split('\t')[1])[0]["transcription"]
                print(label)
                f_s.writelines(str(img_name) + '\t' + str(label) + '\n')
            print('写入完成')

def generate_cropimages_from_txt(base_dir, save_dir):
    txt_dir = f'{base_dir}/test.txt'
    with open(txt_dir, 'r') as f:
        lines = f.readlines()
        for line in lines:
            img_name = line.split('\t')[0]
            new_img_name = line.split('\t')[0].replace('img', 'crop')
            label = eval(line.split('\t')[1])[0]["points"]
            label_np = np.array(label).astype(int)
            # print(img_name)
            # print(label)

            img_tmp = cv2.imread(f'{base_dir}/{img_name}')
            if img_tmp is None:
                print('读取图片为空')
                continue
            ori_im = np.copy(img_tmp)
            left_top = np.array(label_np).min(axis=0)
            right_bottom = np.array(label_np).max(axis=0)
            # print(left_top, right_bottom)
            y0, y1, x0, x1 = left_top[1], right_bottom[1], left_top[0], right_bottom[0]
            # print(y0, y1, x0, x1)
            cropped = ori_im[y0:y1, x0:x1]
            save_img = f'{save_dir}/{new_img_name}'
            cv2.imwrite(save_img, cropped)
        print(f'共生成{len(lines)}张图片')



if __name__ == '__main__':
    base_dir = '/Users/clustar/Desktop/项目/车牌识别/字符识别数据汇总/licenseplate_new/det/test'
    save_dir = '/Users/clustar/Desktop/项目/车牌识别/字符识别数据汇总/licenseplate_new/rec/test'
    generate_croplabel_from_txt(base_dir, save_dir)
    generate_cropimages_from_txt(base_dir, save_dir)