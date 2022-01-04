import cv2 as cv
import argparse
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from pathlib import Path

# parser = argparse.ArgumentParser(
#     description='This sample shows how to define custom OpenCV deep learning layers in Python. '
#                 'Holistically-Nested Edge Detection (https://arxiv.org/abs/1504.06375) neural network '
#                 'is used as an example model. Find a pre-trained model at https://github.com/s9xie/hed.')
# parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')
# parser.add_argument('--prototxt', help='Path to deploy.prototxt', required=True)
# parser.add_argument('--caffemodel', help='Path to hed_pretrained_bsds.caffemodel', required=True)
# parser.add_argument('--width', help='Resize input image to a specific width', default=256, type=int)
# parser.add_argument('--height', help='Resize input image to a specific height', default=256, type=int)
# parser.add_argument('--savefile', help='Specifies the output video path', default='output.mp4', type=str)
# args = parser.parse_args()

prototxt_dir = 'deploy.prototxt'
caffemodel_dir = 'hed_pretrained_bsds.caffemodel'


class CropLayer(object):
    def __init__(self, params, blobs):
        self.xstart = 0
        self.xend = 0
        self.ystart = 0
        self.yend = 0

    # Our layer receives two inputs. We need to crop the first input blob
    # to match a shape of the second one (keeping batch size and number of channels)
    def getMemoryShapes(self, inputs):
        inputShape, targetShape = inputs[0], inputs[1]
        batchSize, numChannels = inputShape[0], inputShape[1]
        height, width = targetShape[2], targetShape[3]

        self.ystart = int((inputShape[2] - targetShape[2]) / 2)
        self.xstart = int((inputShape[3] - targetShape[3]) / 2)
        self.yend = self.ystart + height
        self.xend = self.xstart + width

        return [[batchSize, numChannels, height, width]]

    def forward(self, inputs):
        return [inputs[0][:, :, self.ystart:self.yend, self.xstart:self.xend]]


# Load the model.
net = cv.dnn.readNetFromCaffe(prototxt_dir, caffemodel_dir)
cv.dnn_registerLayer('Crop', CropLayer)


def generate_edge(img_dir):
    image = cv.imread(img_dir)
    img_width = 1920
    img_hight = 1080
    #
    image = cv.resize(image, (img_width, img_hight))

    inp = cv.dnn.blobFromImage(image, scalefactor=1.0, size=(img_width, img_hight),
                               mean=(104.00698793, 116.66876762, 122.67891434),
                               swapRB=False, crop=False)
    net.setInput(inp)
    # edges = cv.Canny(image,image.shape[1],image.shape[0])
    out = net.forward()

    out = out[0, 0]
    # out = cv.resize(out, (image.shape[1], image.shape[0]))
    out = cv.resize(out, (3840, 2160))

    # print(out.shape)

    kernel1 = np.ones((4, 4), dtype=np.uint8)
    erosion = cv.erode(out, kernel1, iterations=1)

    out = cv.cvtColor(erosion, cv.COLOR_GRAY2BGR)

    out = 255 * out
    out = out.astype(np.uint8)
    # out = cv.resize(out, (3840, 2160))

    # print(type(out))
    # print(np.max(out))
    # print(np.min(out))
    # print(out.shape)
    # print(image.shape)
    # con = np.concatenate((image, out), axis=1)
    # cv.imwrite('out.jpg',con)



    savename = str(img_dir).replace('car', 'edge')
    cv.imwrite(savename, out)
    print("边缘图像已保存")





if __name__ == '__main__':
    base_path = Path('/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/test/car')
    image_list = glob(f'{base_path}/*')
    print(len(image_list))
    for img in image_list:
        generate_edge(img)

    pass

