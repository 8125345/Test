import cv2
import numpy as np
import requests
from glob import glob
from pathlib import Path



def process_car(img_dir):
    file = {'img_file': open(img_dir, 'rb')}
    result = requests.post('http://172.16.0.165:15004/jsl/truck_detect', files=file).json()
    image = cv2.imread(img_dir)
    contours = result['data']
    print(image.shape)
    mask = np.zeros(image.shape, np.uint8)
    cv2.fillPoly(mask, [np.array(contours)], (255, 255, 255))

    # alpha = 0.8
    # beta = 1-alpha
    # gamma = 0
    # img_add = cv2.addWeighted(image, alpha, mask, beta, gamma)
    car = cv2.bitwise_and(image, mask)
    return car

    # cv2.imshow("contours", car)
    # cv2.waitKey()


if __name__ == '__main__':
    base_path = Path('/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/test/image')
    image_list = glob(f'{base_path}/*')
    print(len(image_list))
    for img in image_list:
        car = process_car(img)
        save_dir = img.replace('image', 'car')
        cv2.imwrite(save_dir, car)

