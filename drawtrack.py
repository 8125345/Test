import cv2

import numpy as np
from time import *

np.set_printoptions(threshold=np.inf)

# point_size = 3
# point_color = (0, 255, 0)
# thickness = 4

f = open('/Users/clustar/Desktop/项目/金盛兰数据新/吸盘/视频/测试视频/EADT019/第一周期/coor.txt')
# img = cv2.imread('/Users/clustar/Desktop/项目/金盛兰数据新/吸盘/视频/测试视频/EAQX090/第0周期/吸后.png')

coor_list = []
for lines in f.readlines():
    # print(lines)
    lines = (lines.strip('\n'))
    coor = eval(lines)
    coor_list.append(coor)

# for t in range(2, len(coor_list)):
#     for i in range(len(coor_list)):
# d = []
# d1 = {}
# d1[(1,2)] = [1,2,3,4]
# d2 ={}
# d2[(34,2)] = [1,3,4,6]
# d3 = {}
# d3[(1,2)] = [7,8,9,0]
# d.append(d1)
# d.append(d2)
# d.append(d3)
# # print(d)
# for i in d:
#     key = (1, 2)
#     if i.get(key) is not None:
#         print(i.get(key))


    # print(i.keys(), i.values())


# print(d1)
# print(d1.clear())

# print(len(coor_list))

def compare(l1:list):
    if l1 is None:
        return -1
    return max(l1) - min(l1)

# list1 = [1,2,3,4,5,5,5,5,5,5,5,5,6,7,8,9]
# print(list1[-1])

def subarr(list1):
    N = len(list1)
    # print(N)
    left = 0
    right = left + 5
    res = 0
    while right <= N:
        # print(tmp)
        temp = list1[left:right]
        print('temp is:', temp)
        threshold = compare(temp)
        print('threshold is :', threshold)
        if temp and threshold > 0:
            left += 1
            right += 1
        else:
            res = temp
            left += 1
            right += 1
    print(res)

ellip_coor = (2569, 668)
axesSize = (3192, 1191)
rotateAngle = 0
startAngle = 0
endAngle = 360
ellip_color = (0, 0, 255)
ellip_thickness = 4
ellip_lineType = 4

# cv2.ellipse(img, ellip_coor, axesSize, rotateAngle,  startAngle, endAngle, ellip_color, ellip_thickness, ellip_lineType)

point_coor = (2795, 701)
point_size = 3
point_color = (0, 255, 0)
point_thickness = 4
# cv2.circle(img, point_coor, point_size, point_color, point_thickness)

rect_lefttop = (2504, 461)
rect_right_buttom = (3031, 905)
rect_color = (0,255,0)
rect_thickness = 4
rect__lineType = 4
# cv2.rectangle(img, rect_lefttop, rect_right_buttom, rect_color, rect_thickness,rect__lineType)

# cv2.imwrite('/Users/clustar/Desktop/项目/金盛兰数据新/吸盘/视频/测试视频/EAQX090/第0周期/吸后结果.jpg', img)
# cv2.imshow("result", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


def CalCoorDiffVal(coor_list:list):
    if coor_list is None:
        return -1
    arr_tmp = np.array(coor_list)
    max_ = np.amax(arr_tmp, axis=0)
    min_ = np.amin(arr_tmp, axis=0)
    X_Diff = max_[0] - min_[0]
    Y_Diff = max_[1] - min_[1]
    return max(X_Diff, Y_Diff)

# X, Y = CalCoorDiffVal(coor_list)
# print(X, Y)

def findmaxsubarr(coor_list:list):
    DeltaT = 50
    N = len(coor_list)
    print(N)
    left = 0
    right = left + DeltaT
    threshold_list = []
    temp_list = []
    while right <= N:
       temp = coor_list[left:right]
       # print('temp is:', temp)
       temp_list.append(temp)
       threshold = CalCoorDiffVal(temp)
       # print('threshold is :', threshold)
       threshold_list.append(threshold)
       left += 1
       right += 1
    # print('临时列表的长度', len(temp_list))
    # print('阈值的长度', len(threshold_list))
    if len(temp_list) == len(threshold_list):
        Min_threshold = min(threshold_list)
        # print('最小阈值', Min_threshold)
        Min_threshold_idx = threshold_list.index(Min_threshold)
        # print('最小阈值的索引', Min_threshold_idx)
        result_temp = temp_list[Min_threshold_idx]
        # print('最小阈值索引对应的临时列表：', result_temp)
        return result_temp[DeltaT // 2]
    else:
        print('slide windows error')

'''
区域定位测试主程序
'''
# begin_time = time()
# result = findmaxsubarr(coor_list)
# end_time = time()
# run_time = end_time-begin_time
# print('该程序运行时间：', run_time)
# print(result)



# bbox_int = [[1,2,3,4],[2,3,4,5],[4,5,6,7],]
# center_bbox_dict_list = []
# for bbox in bbox_int:
#
#     center_bbox_dict = {}
#     center_bbox_dict[result] = bbox
#     center_bbox_dict_list.append(center_bbox_dict)
#     print(center_bbox_dict)
# # center_bbox_dict.clear()
# print(center_bbox_dict_list)

###异常点处理
# test_sample = [(1,2),(3,4),(5,6),(7,8),(9,10),(20,30),(20,30),(90,100),(11,12),(80,70),(14,15),(16,17),(12,16)]
test_sample = coor_list
print(len(test_sample))
i = 1
while i+1 < len(test_sample):
    np_coor_pre = np.array(test_sample[i-1])
    np_coor_now = np.array(test_sample[i])
    np_coor_last = np.array(test_sample[i+1])
    diff_pre = max(abs(np_coor_now - np_coor_pre))
    diff_last = max(abs(np_coor_last - np_coor_now))
    if diff_pre > 50 and diff_last > 50:
        print(i)
        print(test_sample[i])

    # print(np_coor_pre)
    # print(np_coor_now)
    i += 1

def AbnormalDel(test_sample:list):
    abnormal_thresh = 50
    i = 1
    while i + 1 < len(test_sample):
        np_coor_pre = np.array(test_sample[i - 1])
        np_coor_now = np.array(test_sample[i])
        np_coor_last = np.array(test_sample[i + 1])
        diff_pre = max(abs(np_coor_now - np_coor_pre))
        diff_last = max(abs(np_coor_last - np_coor_now))
        if diff_pre > abnormal_thresh and diff_last > abnormal_thresh:
            print(i)
            print(test_sample[i])
        i += 1






