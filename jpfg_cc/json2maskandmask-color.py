import os
import argparse
import json
import cv2
from labelme import utils
import numpy as np
from glob import glob
import PIL.Image
from pathlib import Path


def json2mask_multi(json_path, label_list=None, overlay_flag=False):
    """The multiple labels of a json file tranform to the corresponding mask image

    Args:
        json_path (str): the path of label json file
        label_list (list): select labels to generate corresponding mask image

    Returns:
        [array]: mask array, shape=(H, W), type=np.uint8, 1 add the label index
        of label_list  means ROI. eg: label_list=['zz', 'cl', 'cc', ], 1 means zz ROI,
        2 means cl ROI, 3means cl ROI
    """
    if label_list is None:
        label_list = ['zz', 'cl', 'cc']

    with open(json_path, 'r', errors='ignore') as f:
        label = json.load(f)
        f.close()
    annotation_dict = {}
    polygons = label['shapes']
    for label_name in label_list:
        for polygon in polygons:
            mask_label_name = polygon['label']
            if label_name == mask_label_name:
                points = np.array(polygon['points']).astype(np.int32)
                if label_name in annotation_dict:
                    annotation_dict[label_name].append(points)
                else:
                    annotation_dict[label_name] = [points]
    if overlay_flag:
        mask = np.zeros((label['imageHeight'], label['imageWidth']),
                        dtype=np.uint8)
    else:
        mask = np.zeros((label['imageHeight'], label['imageWidth'], 3),
                        dtype=np.uint8)
    for anno_key, anno_list in annotation_dict.items():
        if len(anno_list):
            cv2.fillPoly(mask, anno_list, label_list.index(anno_key))
    return mask

def generate_label_colormap():
    colormap = np.zeros((256, 3), dtype=int)
    ind = np.arange(256, dtype=int)
    for shift in reversed(range(8)):
        for channel in range(3):
            colormap[:, channel] |= ((ind >> channel) & 1) << shift
        ind >>= 3
    return colormap

def label2color(mask):
    if mask.ndim != 2:
        raise ValueError('Expect 2-D input mask')
    colormap = generate_label_colormap()
    if np.max(mask*3) >= len(colormap):
        raise ValueError('mask value too large.')
    return colormap[mask*3]         # 3倍的颜色映射间隔


if __name__ == '__main__':
    classes = ['background', 'jpfg_cc']
    base_path = '/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/train/json'
    mask_path = Path(base_path).parent / 'mask'
    mask_path.mkdir(parents=True, exist_ok=True)
    print(mask_path)
    json_list = glob(f'{base_path}/*')
    # print(json_list)
    for i in json_list:
        maskname = Path(i).stem
        # print(maskname)
        mask = json2mask_multi(i, label_list=classes)
        save_path = mask_path / f'{maskname}.png'
        cv2.imwrite(str(save_path), mask)
    print("json转mask完成")

    color_dir = Path(base_path).parent / 'color-mask'
    print(color_dir)
    color_dir.mkdir(parents=True, exist_ok=True)

    mask_list = glob(f'{mask_path}/*')
    mask_list = sorted(mask_list)
    for mask in mask_list:
        mask_img = cv2.imread(mask)[..., 0]
        mask_color = label2color(mask_img)
        cv2.imwrite(mask.replace('mask', 'color-mask'), mask_color)



