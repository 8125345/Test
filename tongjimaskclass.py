import pandas as pd
import numpy as np
from pathlib import Path
np.set_printoptions(threshold=np.inf)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

from collections import Counter

from glob import glob
import cv2
# 统计每个类别的像素值
def statistics_class_pix(mask):

    mask_img = cv2.imread(mask)
    # # 转化格式
    mask_reshape = mask_img.reshape(-1, 3)[:, 1]
    # # 统计第一张图像的每个类别的pix数量
    pix_count = Counter(mask_reshape)
    return pix_count

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





if __name__ == "__main__":

    """
    批量将mask图转成彩色
    
    base_dir = '/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长/gt-mask'
    color_dir = Path(base_dir).parent / 'pre-color-mask'
    print(color_dir)
    color_dir.mkdir(parents=True, exist_ok=True)
    # save_path = '/Users/clustar/Desktop/项目/金盛兰数据_料件/评估集测试/color-mask/'
    mask_list = glob(f'{base_dir}/*')
    mask_list = sorted(mask_list)
    sum_counter = Counter()
    # pix_num = {}
    for mask in mask_list:
        mask_img = cv2.imread(mask)[..., 0]
        mask_color = label2color(mask_img)
        cv2.imwrite(mask.replace('pre-mask', 'pre-color-mask'), mask_color)
    """
    mask = '/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长/gt-mask/EAFE703_1_20210825085926-gtmask.png'
    # mask_img = cv2.imread(mask)
    mask_img = cv2.imread(mask)[..., 0]
    print(mask_img.shape)

    mask_color = label2color(mask_img)
    print(mask_color.shape)
    cv2.imwrite('/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长/EAFE703_1_20210825085926-gtcolormask.png', mask_color)


    # cv2.imshow("result", mask_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()







'''
    统计mask像素个数
    #     pix_num = statistics_class_pix(mask)
    #     sum_counter += pix_num
    # print(sum_counter)
    # print(len(mask_list))
'''




