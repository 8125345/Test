import cv2 as cv
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

mask = cv.imread('/Users/clustar/PycharmProjects/gen_dateset/data/jsl_dataset/evaluate/' 
                'ann_dir/labels_multiseg/EAAB887_2_20210704130126.png',0)
img = cv.imread('/Users/clustar/Desktop/项目/金盛兰数据/20210704/EAAB887/EAAB887_2_20210704130126.jpg',1)
# gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# print(img)
# print(img.shape)
# # print(gray.shape)
#
print(mask.shape)
hest = np.zeros([25],dtype = np.int32)
Xlenth = mask.shape[1]   #图片列数，宽
Ylenth = mask.shape[0]   #图片行数，高
CLASS = ['background', 'cgj',
        'gyfg', 'train', 'mdt', 'jpfg', 'xgsteel', 'sxb',
        'zf1', 'zf2', 'gjyk',
        'jxst', 'ps', 'dbt',
        'zz', 'pf',
        'zf2+', 'mf',
        'zf1_cc', 'zf2_cc', 'cgj_cc', 'jpfg_cc', 'gyfg_cc']

# result = dict([(k, 0) for k in CLASS])
# # print(result)
#
pv = 0
for i in range(Ylenth):
    for j in range(Xlenth):
        # print(mask[i][j])
        pv = mask[i][j]
        # print(pv)
# #         # print(pv.all())
        if pv>0 :
           # print(pv)
           hest[pv] +=1
#
print(hest)

# contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
#
# print(contours)
# cv.drawContours(img,contours,-1, (0, 0, 255), 1)


# img = img[:, :, ::-1]
# img[..., 2] = np.where(mask == 1, 255, img[..., 2])
#
# plt.imshow(img)
# plt.show()


# first_mask_reshape = img.reshape(-1, 3)[:, 1]
#     # 统计第一张图像的每个类别的pix数量
# first_pix_count = Counter(first_mask_reshape)
#     # print('-------------')
# print(first_pix_count,'pixpix------------')







