import shutil
from pathlib import Path

"""
根据txt每行的路径将该文件拷贝到新目录下
"""


base_dir = Path('/home/zhaoliang/yolov5/mf_fire')
filename = base_dir / 'test.txt'
image_dir = base_dir / 'images'
save_dir = base_dir / 'testimage'
save_dir.mkdir(parents=True, exist_ok=True)

with open(filename, 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        image_name = Path(line).name
        # print(image_name)
        test_image_dir = image_dir / image_name
        print(test_image_dir)
        if test_image_dir.exists():
            shutil.copy2(test_image_dir, save_dir)
        else:
            print('test image is not exit')


