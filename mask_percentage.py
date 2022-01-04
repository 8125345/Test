#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/24 下午3:28
# @Author  : zhangyunfei
# @File    : mask_percentage.py
# @Software: PyCharm
import cv2 as cv
from collections import Counter
# from check_data.utils import get_label
import os
from glob import glob
"""
    计算每辆车的mask变化总值
"""

def get_label():
    # 废钢标签
    labels = ['cgj',
                'gyfg', 'train', 'mdt', 'jpfg', 'xgsteel', 'sxb',
                'zf1', 'zf2', 'gjyk',
                'jxst', 'ps', 'dbt',
                'zz', 'pf',
                'zf2+', 'mf',
                'zf1_cc', 'zf2_cc', 'cgj_cc', 'jpfg_cc', 'gyfg_cc']

    label_num = len(labels) + 1  # classes + bg  类别说+背景
    print('')
    # 标签图，给每个标签赋标签值
    class_label_map = {}
    for i, label in enumerate(labels):
        class_label_map[i + 1] = label
        class_label_map[label] = i + 1
    print(class_label_map)
    return class_label_map, labels


# 统计每个类别的像素值
def statistics_class_pix(mask):


    # # 获取mask的路径
    # mask_imgs = os.listdir(mask_dir)
    # # print(mask_imgs[0][:-4])
    # # 由于读取文件是乱序的，需要进行排序
    # mask_imgs.sort(key=lambda x: x[:-4])
    # # print(mask_imgs)
    # mask_paths = []
    # for mask in mask_imgs:
    #     mask_path = os.path.join(mask_dir, mask)
    #     # print(mask_path)
    #     mask_paths.append(mask_path)
    #
    # # 获取标签信息
    # class_label_map, labels = get_label()
    # # 定义每个标签的像素字典，并初始化
    # label_count = {}
    # for i in range(1, 22):
    #     label_count[i] = 0
    # # print(label_count)
    # # 获取第一张mask
    # first_mask = mask_paths[0]
    mask_img = cv.imread(mask)
    # # 转化格式
    mask_reshape = mask_img.reshape(-1, 3)[:, 1]
    # # 统计第一张图像的每个类别的pix数量
    pix_count = Counter(mask_reshape)
    return pix_count


    # # print('-------------')
    # # print(first_pix_count,'pixpix------------')
    # for k, v in label_count.items():
    #     label_count[k] = first_pix_count[k]
    # # print(label_count,'----------')
    # # print(label_count)
    # # 从第二张开始，计算下一帧与上一帧的差别
    # numbers = len(mask_paths)
    # for i in range(numbers - 1):
    #     prev_path = mask_paths[i]
    #     next_path = mask_paths[i + 1]
    #     prev_img = cv.imread(prev_path)
    #     # print(prev_img,'-------')
    #     next_img = cv.imread(next_path)
    #     # 统计两张图像的像素差异
    #     diff_mask = next_img[next_img != prev_img]
    #     # 获取每个类别的像素个数
    #     diff_count = Counter(diff_mask)
    #     # print(prev_path,next_path,diff_count)
    #     for k, v in label_count.items():
    #         # print(label_count[k],diff_count[k],k)
    #         label_count[k] += diff_count[k] / 3
    # # print(label_count)
    # # 计算所有类别的pix的总数
    # pix_total = sum(label_count.values())
    # # print(pix_total)
    # assert pix_total > 0, 'pix is count 0'
    # # print(pix_total)
    # # 计算每个类别的所占比重
    # label_proportion = {
    #     'date': date,
    #     'car': car
    # }
    # for k, v in label_count.items():
    #     # print(class_label_map[k], v / pix_total)
    #     label_proportion[class_label_map[k]] = 100 * (v / pix_total)
    # return label_proportion

if __name__ == "__main__":
    base_dir = '/Users/clustar/Desktop/项目/金盛兰数据新/label_mask'
    mask_list = glob(f'{base_dir}/*/*/*')
    mask_list = sorted(mask_list)
    sum_counter = Counter()
    # pix_num = {}
    for mask in mask_list:
        pix_num = statistics_class_pix(mask)
        sum_counter += pix_num
    print(sum_counter)
    print(len(mask_list))


