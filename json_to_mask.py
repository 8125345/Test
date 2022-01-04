"""
     将标注的json文件转化成mask标签格式
"""
import json
import cv2 as cv
import os
import numpy as np


# 获取文件路径
def travel_path(dir, files=None, extension_list=('jpg',), ignore_files=None):
    """
    :param dir: 文件路径
    :param files: 文件列表
    :param extension_list: 支持的文件格式
    :param ignore_files: 需要过滤的文件
    :return:
    """
    if ignore_files is None:
        ignore_files = []
    if files is None:
        files = []
    # 读取文件列表
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path):
            if '.' in path:
                _, extension = path.rsplit('.', 1)
                if extension.lower() in extension_list and file not in ignore_files:
                    files.append(path)
        elif os.path.isdir(path):
            travel_path(path, files, extension_list, ignore_files)


# labels 标签
def get_label():
    # 废钢标签
    labels = [ 'pf_cc', 'zf1_cc',
                'cgj_cc', 'gyfg_cc',
                'jpfg_cc',  'zf2_cc',
                'train_cc']

    label_num = len(labels) + 1  # classes + bg  类别说+背景
    # 标签图，给每个标签赋标签值
    class_label_map = {}
    for i, label in enumerate(labels):
        class_label_map[i + 1] = label
        class_label_map[label] = i + 1
    print(class_label_map)
    return class_label_map, labels


# 获取label对应的标签值
def get_label_value_from_class_name(label, class_label_map, labels):
    label_value = -1
    is_find = True
    if label not in labels:
        is_find = False
        return is_find, label_value
    label_value = class_label_map[label]
    return is_find, label_value


# json标签 转 mask标签
def json_2_mask(json_path, class_label_map, labels):
    """
    :param json_path: json文件地址
    :param class_label_map: 标签图，类别对应标签
    :param labels: 类别名
    :return:
    """
    # 标签 mask
    mask_img = None
    # 打开json文件
    with open(json_path, 'r', encoding='utf8') as op:
        try:
            json_data = json.load(op)
        except Exception as e:
            print("json load error info as {}".format(e))
            return mask_img
    # print(json_data)
    # 获取图像宽高
    im_h = json_data["imageHeight"]
    im_w = json_data["imageWidth"]
    assert im_h == 2160, "im_h == 2160 is error"
    assert im_w == 3840, "im_w == 3840 is error"

    # 生成空白的mask
    mask_img = np.zeros((im_h, im_w), dtype=np.float32)
    # 获取所有的多边形信息，也就是mask
    polygons = json_data["shapes"]
    for pg in polygons:
        # print(pg)
        label = pg["label"]
        points = pg["points"]
        is_find, label_value = get_label_value_from_class_name(label, class_label_map, labels)
        if is_find:
            label_points = np.array(points).astype(np.int32)
            cv.fillPoly(mask_img, [label_points], label_value)
            # else:
            #     print("label error ", label)
    return mask_img

# 处理每一张图像
def process_each_path(each_path, class_label_map, labels):
    """
    :param each_path: 图像路径
    :param class_label_map: 标签字典
    :param labels: 标签名称
    :return:
    """
    # json_path = each_path.replace(".jpg", ".json")
    json_path = each_path
    # 检查文件
    assert os.path.isfile(json_path)
    return json_2_mask(json_path, class_label_map, labels)


# 生成mask主函数
def mask_main():
    # json 标注文件路径
    base_dir = "/Users/clustar/Desktop/项目/金盛兰数据_料件/超长测试mask"
    # 多料件mask目录
    mask_dir = "/Users/clustar/Desktop/项目/金盛兰数据_料件/超长测试mask结果"
    files = []
    # 加载文件
    travel_path(base_dir, files, extension_list=("json",))
    # print(files[:3])
    # 获取标签信息
    class_label_map, labels = get_label()
    for i, item in enumerate(files):
        print("begin process id:{}, path:{}".format(i, item))
        # 获取多料件mask和车厢主体mask
        # process_each_path(item, class_label_map, labels)
        mask_img = process_each_path(item, class_label_map, labels)
        if mask_img is not None:
            mask_path = item.replace(base_dir, mask_dir).replace(".json", ".png")
            # 获取新的目录
            new_mask_dir = os.path.dirname(mask_path)
            # print(new_mask_dir)
            # 创建文件夹，如果路径目录不存在
            os.makedirs(new_mask_dir, exist_ok=True)
            cv.imwrite(mask_path, mask_img)

mask_main()
