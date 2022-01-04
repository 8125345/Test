"""
    计算标注的mask得出的类别权重，对比老陈给的类别权重
"""
import json
import cv2 as cv
import numpy as np
import os
from collections import Counter


# labels 标签
def get_label():
    # 废钢标签
    labels = ["gjjj", "10mm", "8mm", "6mm", "5mm", "4mm", "3mm", "2mm", "1_5mm", "gj1", "gj2", "gj3",
              "st1", "st2", "st3", "dbl1", "dbl2", "dbl3", "mf", "cgw"]

    label_num = len(labels) + 1  # classes + bg  类别说+背景
    # 标签图，给每个标签赋标签值
    class_label_map = {}
    for i, label in enumerate(labels):
        class_label_map[i + 1] = label
        class_label_map[label] = i + 1
    # print(class_label_map)
    return class_label_map, labels


# 统计每个类别的像素值
def statistics_class_pix(masks_path):
    # 定义每个标签的像素字典，并初始化
    label_count = {}
    for i in range(1, 19):
        label_count[i] = 0
    # print(label_count)
    # 获取第一张mask
    first_mask = masks_path[0]
    first_mask_read = cv.imread(first_mask)
    # 转化格式
    first_mask_reshape = first_mask_read.reshape(-1, 3)[:, 1]
    # 统计第一张图像的每个类别的pix数量
    first_pix_count = Counter(first_mask_reshape)
    # print('-------------')
    # print(first_pix_count,'pixpix------------')
    for k, v in label_count.items():
        label_count[k] = first_pix_count[k]
    # print(label_count,'----------')
    # print(label_count)
    # 从第二张开始，计算下一帧与上一帧的差别
    numbers = len(masks_path)
    for i in range(numbers - 1):
        prev_path = masks_path[i]
        next_path = masks_path[i + 1]
        prev_img = cv.imread(prev_path)
        # print(prev_img,'-------')
        next_img = cv.imread(next_path)
        # 统计两张图像的像素差异
        diff_mask = next_img[next_img != prev_img]
        # 获取每个类别的像素个数
        diff_count = Counter(diff_mask)
        # print(prev_path,next_path,diff_count)
        for k, v in label_count.items():
            # print(label_count[k],diff_count[k],k)
            label_count[k] += diff_count[k] / 3
        # print(label_count)
    return label_count


# 比较函数
def compare_main():
    #  读取需要计算的数据，json文件
    with open('data/check_data.json', 'r', encoding='utf8') as fp:
        check_data = json.load(fp)
    # 获取标签信息
    class_label_map, labels = get_label()
    # print(class_label_map)
    # 获取计算结果
    check_result = []
    for i,item in enumerate(check_data):
        print("begin process id:{}, path:{}".format(i, item))
        # print(item)
        mark_date = item['date']
        car_num = item['car_num']
        car_path = str(mark_date) + '/' + car_num
        # 获取每辆车的路径
        mark_dir = os.path.join('data/masks/mask', car_path)
        mask_imgs = os.listdir(mark_dir)
        # print(mask_imgs[0][:-4])
        # 由于读取文件是乱序的，需要进行排序
        mask_imgs.sort(key=lambda x: x[:-4])
        # print(mask_imgs)
        mask_paths = []
        for mask in mask_imgs:
            mask_path = os.path.join(mark_dir, mask)
            # print(mask_path)
            mask_paths.append(mask_path)
        label_count = statistics_class_pix(mask_paths)
        # print(label_count)
        # 计算所有类别的pix的总数
        pix_total = sum(label_count.values())
        if pix_total<1:
            print('error---------------')
            continue
        # print(pix_total)
        # 计算每个类别的所占比重
        label_proportion = {}
        for k, v in label_count.items():
            # print(class_label_map[k], v / pix_total)
            label_proportion[class_label_map[k]] = 100 * (v / pix_total)
        label_proportion['date'] = mark_date
        label_proportion['car_num'] = car_num
        check_result.append(label_proportion)

    with open('data/check_result.json', 'w', encoding='utf8') as fp:
        fp.write(json.dumps(check_result))

def test():
    # 获取标签信息
    class_label_map, labels = get_label()
    # print(class_label_map)
    # 生成好的mask彩色
    # base_dir = "/Users/clustar/clustar-zyf/cg_seg_data/masks/20201203/CAAT010"
    base_dir = 'data/masks/mask/20210116/CT17190'
    # 获取每辆车的路径
    mask_imgs = os.listdir(base_dir)
    # print(mask_imgs[0][:-4])
    # 由于读取文件是乱序的，需要进行排序
    mask_imgs.sort(key=lambda x: x[:-4])
    print(mask_imgs)
    mask_paths = []
    for mask in mask_imgs:
        mask_path = os.path.join(base_dir, mask)
        mask_paths.append(mask_path)
    label_count = statistics_class_pix(mask_paths)
    # 计算所有类别的pix的总数
    pix_total = sum(label_count.values())
    # print(pix_total)
    # 计算每个类别的所占比重
    label_proportion = {}
    for k, v in label_count.items():
        # print(class_label_map[k], v / pix_total)
        label_proportion[class_label_map[k]] = 100 * (v / pix_total)
    label_proportion['date'] = '20210312'
    label_proportion['car_num'] = 'CACA302'
    print(label_proportion)


compare_main()
# test()

