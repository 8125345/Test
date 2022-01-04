import argparse
import os
import datetime

import cv2
import numpy as np
import pandas as pd
import json

from tqdm import tqdm
from glob import glob
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
            cv2.fillPoly(mask, anno_list, label_list.index(anno_key) + 1)

    # output = np.zeros((label['imageHeight'], label['imageWidth'], len(label_list)), dtype=np.uint8)
    # output[..., 0] = mask[..., 0]

    return mask



def generate_label_colormap():
    """generate mutil segment label color map

    Returns:
        [dict]: label Colormap
    """
    colormap = np.zeros((256, 3), dtype=int)
    ind = np.arange(256, dtype=int)

    for shift in reversed(range(2)):
        for channel in range(3):
            colormap[:, channel] |= ((ind >> channel) & 1) << shift
        ind >>= 3

    return colormap


def label2color(mask):
    """map color to mask array(2D) by the label colormap

    Args:
        mask (uint8): the mask image array(2D)

    Raises:
        ValueError: the mask is not 2D array
        ValueError: the element value of the array is larger than colormap maximum entry.

    Returns:
        [2D array]: mask array with floating type. The element of the array is
        the color indexed by the corresponding element in the input mask to the colormap.
    """
    if mask.ndim != 2:
        raise ValueError('Expect 2-D input mask')

    colormap = generate_label_colormap()

    if np.max(mask*3) >= len(colormap):
        raise ValueError('mask value too large.')

    return colormap[mask*3]         # 3倍的颜色映射间隔


def generate_overlay_by_mask(ori_img_path,
                             overlay_path,
                             foreground,
                             re_size=None,
                             multi_flag=True):
    """generate overlay image

    Args:
        ori_img_path (str): origin image path
        overlay_path (str): overlay image save path
        multi_flag (bool, optional): whether plots multiple annotation. Defaults to True.
    """
    background = cv2.imread(ori_img_path)
    if multi_flag:
        if len(foreground.shape) != 2:
            foreground = foreground[..., 0]
        foreground = label2color(mask=foreground)
        overlay_image = cv2.addWeighted(background,
                                        0.6,
                                        foreground,
                                        0.4,
                                        0,
                                        dtype=cv2.CV_32F)
    else:
        overlay_image = cv2.addWeighted(background,
                                        0.4,
                                        foreground,
                                        0.2,
                                        0,
                                        dtype=cv2.CV_32F)
    if re_size:
        h, w = overlay_image.shape[:2]
        overlay_image = cv2.resize(overlay_image, (re_size, round(re_size * h/w)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(overlay_path, overlay_image)

if __name__ == '__main__':
    classes = ['jpfg_cc']
    base_path = Path('/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长/test')
    file_list = glob(f'{base_path}/*/*/*')
    mask_save_dir = Path('/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长/gt-mask')
    mask_save_dir.mkdir(parents=True, exist_ok=True)
    json_list = [json_ for json_ in file_list if json_.endswith('json')]
    json_list = sorted(json_list)
    print(len(json_list))
    for i in json_list:
        maskname = Path(i).stem
        mask = json2mask_multi(i, label_list=classes)
        # print(mask.shape)
        cv2.imwrite(f'{mask_save_dir}/{maskname}-gtmask.png', mask)


