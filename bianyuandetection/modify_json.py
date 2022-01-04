from glob import glob
import json
from collections import Counter
import shutil
from pathlib import Path
import numpy as np
from img2base64 import imgEncode

base_dir = '/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/test/'

file_list = glob(f'{base_dir}/edge_json/*')
file_list = sorted(file_list)

for js in file_list:
    img_dir = js.replace('edge_json', 'edge').replace('.json', '.jpg')
    with open(js, 'r+', encoding='utf8') as fp:
        check_data = json.load(fp)
        check_data['imageData'] = str(imgEncode(img_dir))
        fp.seek(0)  # rewind
        json.dump(check_data, fp, ensure_ascii=False)
        fp.truncate()







