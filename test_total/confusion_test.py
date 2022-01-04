import cv2
import numpy as np
from cc_yuce.evaluate import CalMatrixSecond
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import type_of_target
from skimage import io
from collections import Counter
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def get_confusion_matrix(pred, ground_truth, n_classes):
    # get confusion matrix
    # remove classes from unlabeled pixels in ground_truth and predict (同FCN中score.py的fast_hist()函数)
    mask = (ground_truth >= 0) & (ground_truth < n_classes)
    label = n_classes * ground_truth[mask].astype('int') + pred[mask]
    confusion_matrix = np.bincount(label, minlength=n_classes ** 2)
    confusion_matrix = confusion_matrix.reshape(n_classes, n_classes)
    return confusion_matrix


img_gt = cv2.imread('./cc_yuce/gt.png', cv2.IMREAD_COLOR)
img_pre = cv2.imread('./cc_yuce/pre.png')

mask_gt_reshape = img_gt.reshape(-1, 3)[:, 1]
pix_count_gt = Counter(mask_gt_reshape)
print(pix_count_gt)

mask_pre_reshape = img_pre.reshape(-1, 3)[:, 1]
pix_count_pre = Counter(mask_pre_reshape)
print(pix_count_pre)


c1 = get_confusion_matrix(mask_pre_reshape, mask_gt_reshape, 8)
print(c1)
#
# c2 = confusion_matrix(mask_gt_reshape, mask_pre_reshape)
# print(c2)

# print(np.sum(c1, axis=1))
#
# freq = np.sum(c1, axis=1) / np.sum(c1)
# print(freq)



classes_dict = {'cls_8': [
                'background',
                'pf_cc', 'zf1_cc',
                'cgj_cc', 'gyfg_cc',
                'jpfg_cc', 'zf2_cc',
                'train_cc',
            ]}

# print(classes_dict.items())
final_eval_8_multiseg = pd.DataFrame()

for key, classes_multiseg in classes_dict.items():
    iou_classes_multiseg = [f'iou_{col}' for col in classes_multiseg]

    eval_iou = CalMatrixSecond(c1)
    eval_iou.cal_freq()
    eval_iou.class_pixel_iou()
    eval_iou.each_weighted_iou()
    eval_iou.miou()
    eval_iou.frequency_weighted_iou()
    class_iou = pd.DataFrame([eval_iou.each_class_iou], columns=iou_classes_multiseg)
#
#
    weight_cols = [f"weight_{col.split('_')[0]}_{col.split('_')[1]}" for col in classes_multiseg if col not in 'background']

    freq_weight = pd.DataFrame([eval_iou.freq], columns=weight_cols)
    print(freq_weight)
#     class_iou['fwiou'] = eval_iou.fwiou
#     class_iou['miou'] = eval_iou.miou
#     # print(class_iou)
#     eval_multiseg = pd.concat([class_iou, freq_weight], axis=1)
    # print(eval_multiseg)


# eval_df = pd.read_csv('./cc_yuce/1.csv')
# # print(eval_df)
# eval_df_ = eval_df.groupby(['date_carid'])
# # print(eval_df_)
# avg_eval_df = eval_df_.mean()
# print(round(avg_eval_df, 4))
# round(avg_eval_df, 4).to_csv('./cc_yuce/2.csv', index=True)
# # print(avg_eval_df.mean())



