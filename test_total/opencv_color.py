import cv2
import numpy as np

# I = np.zeros((100, 100), dtype=np.uint8)
# I = cv2.cvtColor(I, cv2.COLOR_GRAY2BGR)
#
# I[:, :, 0] = 128
# I[:, :, 1] = 64
# I[:, :, 2] = 128
#
# cv2.imshow("result", I)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


image = cv2.imread('/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/test/crop/EARY327_2_20210818072352.png')

print(image.shape)



point_coor = (2795, 701)
point_size = 3
point_color = (0, 255, 0)
point_thickness = 4
cv2.circle(img, point_coor, point_size, point_color, point_thickness)






