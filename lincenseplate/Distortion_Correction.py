import cv2
import numpy as np





def perspective():
    test_image = '/Users/clustar/Desktop/项目/车牌识别/12月份预测结果/det_results/chegnshi_1cp_20211207033252_5795366.jpg'

    img = cv2.imread(test_image)
    rows, cols = img.shape[:2]

    # original pts
    '''
    [[896, 330], [1107, 387], [1076, 500], [866, 443]]
    '''
    pts_o = np.float32([[896, 330], [1107, 387], [1076, 500], [866, 443]])  # 这四个点为原始图片上数独的位置




    pts_d = np.float32(confirmlocation())  # 这是变换之后的图上四个点的位置

    # get transform matrix
    M = cv2.getPerspectiveTransform(pts_o, pts_d)
    # apply transformation
    dst = cv2.warpPerspective(img, M, (2560, 1440))  # 最后一参数是输出dst的尺寸。可以和原来图片尺寸不一致。按需求来确定

    cv2.imshow('img', img)
    cv2.imshow('dst', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def confirmlocation():
    init_loc = np.array([[896, 330], [1107, 387], [1076, 500], [866, 443]])
    dst_max = init_loc.max(axis=0)
    dst_min = init_loc.min(axis=0)
    dh = dst_max[1] - dst_min[1]
    dw = dst_max[0] - dst_min[0]
    left_up = dst_min
    left_bottom = [dst_min[0], dst_max[1]]
    right_bottom = dst_max
    right_up = [dst_max[0], dst_min[1]]
    dst_coor = [left_up, right_up, right_bottom, left_bottom]
    print(init_loc)
    print(dst_max)
    print(dst_min)
    print(dh)
    print(dw)
    return dst_coor

confirmlocation()


# perspective()



# if __name__ == '__main__':
#
#     test_image = '/Users/clustar/Desktop/项目/车牌识别/12月份预测结果/det_results/chegnshi_1cp_20211207033252_5795366.jpg'
#     img = cv2.imread(test_image)
#
#     point_coor = (866, 443)
#     point_size = 3
#     point_color = (0, 255, 0)
#     point_thickness = 4
#     cv2.circle(img, point_coor, point_size, point_color, point_thickness)
#     cv2.imshow("result", img)
#     cv2.waitKey(0)



