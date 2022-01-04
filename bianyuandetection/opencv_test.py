import cv2
import numpy as np


def draw_contours(img, cnts):  # conts = contours
    img = np.copy(img)
    img = cv2.drawContours(img, cnts, -1, (0, 255, 0), 2)
    return img


def draw_min_rect_circle(img, cnts):  # conts = contours
    img = np.copy(img)

    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # blue

        min_rect = cv2.minAreaRect(cnt)  # min_area_rectangle
        min_rect = np.int0(cv2.boxPoints(min_rect))
        cv2.drawContours(img, [min_rect], 0, (0, 255, 0), 2)  # green

        # (x, y), radius = cv2.minEnclosingCircle(cnt)
        # center, radius = (int(x), int(y)), int(radius)  # center and radius of minimum enclosing circle
        # img = cv2.circle(img, center, radius, (0, 0, 255), 2)  # red
    return img


def draw_approx_hull_polygon(img, cnts):
    img = np.copy(img)
    img1 = np.zeros(img.shape, dtype=np.uint8)

    # cv2.drawContours(img, cnts, -1, (255, 0, 0), 2)  # blue

    min_side_len = img1.shape[0] / 32  # 多边形边长的最小值 the minimum side length of polygon
    min_poly_len = img1.shape[0] / 16  # 多边形周长的最小值 the minimum round length of polygon
    min_side_num = 3  # 多边形边数的最小值
    min_area = 5000.0  # 多边形面积的最小值
    max_area = 45000.0
    approxs = [cv2.approxPolyDP(cnt, 1, True) for cnt in cnts]  # 以最小边长为限制画出多边形
    # print(len(approxs))
    # approxs = [approx for approx in approxs if cv2.arcLength(approx, True) > min_poly_len]  # 筛选出周长大于 min_poly_len 的多边形
    # approxs = [approx for approx in approxs if len(approx) > min_side_num]  # 筛选出边长数大于 min_side_num 的多边形
    # for approx in approxs:
    #     print(cv2.contourArea(approx))
    approxs = [approx for approx in approxs if min_area < cv2.contourArea(approx) < max_area]  # 筛选出面积大于 min_area_num 的多边形
    # approxs = [approx for approx in approxs if min_area < cv2.contourArea(approx)]
    # Above codes are written separately for the convenience of presentation.
    cv2.polylines(img, approxs, True, (0, 255, 0), 2)  # green

    hulls = [cv2.convexHull(cnt) for cnt in cnts]
    hulls = [hull for hull in hulls if cv2.contourArea(hull) > min_area]
    # cv2.polylines(img, hulls, True, (0, 0, 255), 2)  # red

    # for cnt in cnts:
    #     cv2.drawContours(img, [cnt, ], -1, (255, 0, 0), 2)  # blue
    #
    #     epsilon = 0.02 * cv2.arcLength(cnt, True)
    #     approx = cv2.approxPolyDP(cnt, epsilon, True)
    #     cv2.polylines(img, [approx, ], True, (0, 255, 0), 2)  # green
    #
    #     hull = cv2.convexHull(cnt)
    #     cv2.polylines(img, [hull, ], True, (0, 0, 255), 2)  # red
    return img


def fillHole255(im_in):
    im_floodfill = im_in.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_in.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0, 0), 200, cv2.FLOODFILL_FIXED_RANGE);

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground.
    im_out = im_in | im_floodfill_inv

    return im_out

def fillHole0(im_in):
    im_floodfill = im_in.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_in.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0, 0), 0, cv2.FLOODFILL_FIXED_RANGE);

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground.
    im_out = im_in | im_floodfill_inv

    return im_out

def run():
    img_width = 1100
    img_hight = 1400
    img_dir = '/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/test/edge/EL6B900_2_20210609142107-edge.jpg'
    # image_dir = '/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/test/crop/EARY327_2_20210818070924.png'
    image_dir = img_dir.replace('edge', 'crop').replace('-crop.jpg', '.png')
    print(image_dir)
    save_dir = img_dir.replace('edge', 'result')
    img_new = cv2.imread(image_dir)
    img_new = cv2.resize(img_new, ((img_width, img_hight)))
    image = cv2.imread(img_dir)  # a black objects on white image is better
    image = np.copy(image)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # canny,laplacian边缘检测
    # Cannythresh = cv2.Canny(image_gray, 255, 255)
    # Ksize = 5
    # laplacian = cv2.Laplacian(image_gray, cv2.CV_8U, ksize=Ksize)
    # laplacian = cv2.convertScaleAbs(laplacian)

    # dst = cv2.equalizeHist(image_gray)
    # img_gauss = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                   cv2.THRESH_BINARY, 5, 3)
    # ret, thresh1 = cv2.threshold(image_gray,
    #                              127,
    #                              255, cv2.THRESH_BINARY)

    kernel1 = np.ones((3, 3), dtype=np.uint8)
    erosion = cv2.erode(image_gray, kernel1, iterations=1)
    # kernel2 = np.ones((3, 3), dtype=np.uint8)
    # dilate = cv2.dilate(laplacian, kernel2, 1)
    # opening = cv2.morphologyEx(Cannythresh, cv2.MORPH_OPEN, kernel1, 1)

    # medianBlur_r = cv2.medianBlur(Cannythresh, 3)
    # bilateralFilter_r = cv2.bilateralFilter(erosion, 7, 100, 100)  # 双边滤波
    # GaussianBlur_r = cv2.GaussianBlur(Cannythresh, (5, 5), 0, 0)

    # out_image255 = fillHole255(thresh1)
    # out_image0 = fillHole0(out_image255)

    # gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # print(Cannythresh.shape)
    # out_image255 = fillHole255(bilateralFilter_r)
    # out_image0 = fillHole0(bilateralFilter_r)

    contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(type(contours))
    # print(len(contours))
    print(contours)
    # print(hierarchy, ":hierarchy")
    """
    [[[-1 -1 -1 -1]]] :hierarchy  # cv2.Canny()

    [[[ 1 -1 -1 -1]
      [ 2  0 -1 -1]
      [ 3  1 -1 -1]
      [-1  2 -1 -1]]] :hierarchy  # cv2.threshold()
    """

    imgs = [
        # laplacian,
        # bilateralFilter_r,
        # GaussianBlur_r,

        # medianBlur_r,
        # dilate,
        # opening,
        # thresh1,
        # out_image0,
        # out_image255,
        # img_gauss,
        # dst,
        # image_gray,
        # Cannythresh,
        # draw_contours(image, contours)
        # draw_min_rect_circle(image, contours),
        # erosion,
        draw_approx_hull_polygon(img_new, contours),
    ]

    for img in imgs:
        # print(id(img))
        # cv2.imwrite(save_dir, img)
        # cv2.imshow("contours", img)
        # cv2.waitKey()
        pass


if __name__ == '__main__':
    run()
    # img_dir = '/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/test/crop/EARY327_2_20210818072352.png'
    # image = cv2.imread(img_dir)
    # new = cv2.resize(image, (480, 320))
    # cv2.imwrite('/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/test/crop/1.png', new)
    #
    # new2 = cv2.resize(new, (776, 1107))
    # cv2.imwrite('/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/test/crop/2.png', new2)


pass
