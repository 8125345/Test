import albumentations as A
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import argparse
import json
from labelme import utils
from glob import glob
from matplotlib.font_manager import FontProperties
# plt.rcParams['font.family'] = ['sans-serif']
# plt.rcParams['font.sans-serif'] = ['SimHei']
#
# im = '/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/test_ori/20210818/EARY327/EARY327_2_20210818070206.jpg'

# font = FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc', size=16)
#解决中文显示问题
# plt.rcParams['font.sans-serif']=['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# Read an image with OpenCV and convert it to the RGB colorspace
# image = cv2.imread(im)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# Augment an image
# transformed = A.VerticalFlip(always_apply=False, p=1)(image=image)
# transformed_image = transformed["image"]
# plt.subplot(1, 2, 1)
# plt.title('原图')   #第一幅图片标题
# plt.imshow(image)
# plt.subplot(1, 2, 2)
# plt.title('垂直翻转后的图像')
# plt.imshow(transformed_image)
# plt.show()
# plt.imsave('/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/EARY327_2_20210818070206.jpg', transformed_image)


base_path = Path('/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/train')
data_augmentation = base_path / 'data_augmentation'
VerticalFlip_image = data_augmentation / 'VerticalFlip' / 'image'
VerticalFlip_mask = data_augmentation / 'VerticalFlip' / 'mask'
VerticalFlip_image.mkdir(parents=True, exist_ok=True)
VerticalFlip_mask.mkdir(parents=True, exist_ok=True)
data_augmentation.mkdir(parents=True, exist_ok=True)


HorizontalFlip_image = data_augmentation / 'HorizontalFlip' / 'image'
HorizontalFlip_mask = data_augmentation / 'HorizontalFlip' / 'mask'
HorizontalFlip_image.mkdir(parents=True, exist_ok=True)
HorizontalFlip_mask.mkdir(parents=True, exist_ok=True)
data_augmentation.mkdir(parents=True, exist_ok=True)

"""
垂直翻转
"""

def image_VerticalFlip():
    image_path = base_path / 'image'
    image_list = glob(f'{image_path}/*')
    print(len(image_list))
    for img in image_list:
        imgname = Path(img).stem
        image = cv2.imread(img)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        transformed = A.VerticalFlip(always_apply=False, p=1)(image=image)
        transformed_image = transformed["image"]
        savename = f'{VerticalFlip_image}/{imgname}-VFlip.jpg'
        plt.imsave(savename, transformed_image)
    print("图像垂直翻转完成")

def mask_VerticalFlip():
    mask_path = base_path / 'color-mask'
    mask_list = glob(f'{mask_path}/*')
    print(len(mask_list))
    for mask in mask_list:
        maskname = Path(mask).stem
        imask = cv2.imread(mask)
        imask = cv2.cvtColor(imask, cv2.COLOR_BGR2RGB)
        transformed = A.VerticalFlip(always_apply=False, p=1)(image=imask)
        transformed_mask = transformed["image"]
        savename = f'{VerticalFlip_mask}/{maskname}-VFlip.png'
        plt.imsave(savename, transformed_mask)
    print("mask垂直翻转完成")

"""
水平翻转
"""

def image_HorizontalFlip():
    image_path = base_path / 'image'
    image_list = glob(f'{image_path}/*')
    print(len(image_list))
    for img in image_list:
        imgname = Path(img).stem
        image = cv2.imread(img)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        transformed = A.HorizontalFlip(always_apply=False, p=1)(image=image)
        transformed_image = transformed["image"]
        savename = f'{HorizontalFlip_image}/{imgname}-HFlip.jpg'
        plt.imsave(savename, transformed_image)
    print("图像水平翻转完成")
def mask_HorizontalFlip():
    mask_path = base_path / 'color-mask'
    mask_list = glob(f'{mask_path}/*')
    print(len(mask_list))
    for mask in mask_list:
        maskname = Path(mask).stem
        imask = cv2.imread(mask)
        imask = cv2.cvtColor(imask, cv2.COLOR_BGR2RGB)
        transformed = A.HorizontalFlip(always_apply=False, p=1)(image=imask)
        transformed_mask = transformed["image"]
        savename = f'{HorizontalFlip_mask}/{maskname}-HFlip.png'
        plt.imsave(savename, transformed_mask)
    print("mask水平翻转完成")


if __name__ == "__main__":
    image_VerticalFlip()
    mask_VerticalFlip()
    image_HorizontalFlip()
    mask_HorizontalFlip()










