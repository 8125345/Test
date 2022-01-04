import cv2
from pathlib import Path
# img = cv2.imread("/Users/clustar/Desktop/项目/车牌识别/det_source/20210824001603川AL5827.jpg")
# cv2.imshow("result", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
import matplotlib.pyplot as plt
# import mmcv
# img = ''
# img = mmcv.imread(img)
# img = img.copy()


json_dir = '/Users/clustar/Desktop/项目/车牌识别/一号车位车牌数据/1号车位车牌原始数据/20211207/chegnshi_1cp_20211207033252_5795366.json'


print(Path(json_dir).name)
print(Path(json_dir).stem)




