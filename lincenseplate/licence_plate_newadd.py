import xml.etree.ElementTree as ET
from pathlib import Path
from glob import glob
import shutil
from collections import Counter
import json
"""
车牌数据统计分布：
一、统计出当前数据包含的省份
二、统计出当前数据包含的数字
三、统计出当前数据包含的字母
车牌数据处理：
一、修改图片名称
二、创建train.txt和test.txt：格式为：
   .../img11.jpg\t
   [{"transcription": "车牌内容", 
   "points": [[214.0, 325.0], [235.0, 308.0], [259.0, 296.0], [286.0, 291.0]}]
   文件名和标注信息中间用"\t"分隔：json.dumps编码前的图像标注信息是包含多个字典的list，
   字典中的 points 表示文本框的四个点的坐标(x, y)，从左上角的点开始顺时针排列。 
   transcription 表示当前文本框的文字，当其内容为“###”时，表示该文本框无效，在训练时会跳过。
   如果您想在其他数据集上训练，可以按照上述形式构建标注文件。
"""


"""
旧数据集格式
base_dir = Path('/Users/clustar/Desktop/项目/车牌识别/车牌照片/新增/20210828')
null_xml_list = []
null_json_list = []

"""



def StatisticLicensePlate():
    province_list = []
    letter_number_list = []
    all_file = glob(f'{base_dir}/*')
    print(len(all_file))  #26:198   27: 196
    for file in all_file:
        file_name = Path(file).name
        # print(file_name)
        province = file_name[14:15]
        # print(province)
        province_list.append(province)
        letter_number = file_name[15:21]
        letter_number_list.append(letter_number)

    # print(len(province_list))
    print(list(set(province_list)))  # ['藏', '辽', '青', '鲁', '陕', '吉',
    # '皖', '豫', '黑', '津', '宁', '川', '甘',
    # '冀', '渝', '赣', '新']
    print(len(list(set(province_list))))  # 出现了17个省份

    print(Counter(province_list))  # ({'川': 289, '甘': 18, '青': 17, '陕': 13,
    # '冀': 13, '新': 12, '宁': 11, '渝': 8, '鲁': 10,
    # '豫': 9, '赣': 5, '吉': 4, '皖': 3, '黑': 2,
    # '辽': 2, '藏': 1, '津': 1})
    # print(letter_number_list)
    # for ln in letter_number_list:
    figure_list = []
    for ln in letter_number_list:
        if len(ln) != 6:
            print(ln)
        else:
            for figure in ln:
                figure_list.append(figure)
    # print(figure_list)
    print(set(figure_list))  # 'A','B','C', 'D','E','F', 'G',
    # 'H','J','K','L','M','N',
    # 'P', 'Q', 'R','S','T', 'U','V', 'W','X','Y', 'Z',
    # '2', '1', '5','9','7', '6', '8','4','3','0',

    print(Counter(figure_list))  # '0': 171, '1': 196，'2': 194, '3': 173, '4': 37,
    # '5': 202, '6': 200, '7': 166,'8': 178,'9': 166,
    # 'A': 220, 'B': 38, 'C': 38, 'D': 44,  'E': 35, 'F': 16, 'G': 13,
    # 'H': 19, 'J': 26, 'K': 15, 'L': 20, 'M': 18, 'N': 26,
    #  'P': 15, 'Q': 19, 'R': 30, 'S': 17,  'T': 46,
    # 'U': 23, 'V': 23, 'W': 13, 'X': 20,  'Y': 11， 'Z': 12,


# StatisticLicensePlate()

def FindBadSample():
    all_file = glob(f'{base_dir}/*')
    bad_sample = []  ##用于存放一个文件夹里有超过两个文件的文件
    for file in all_file:
        file_name = Path(file).name
        image_name = file_name[14:]
        child_file = glob(f'{file}/*')
        # print(child_file)
        if len(child_file) != 2:
            print(Path(file).name)
            bad_sample.append(file)
            shutil.move(file, f'/Users/clustar/Desktop/项目/车牌识别/车牌照片/新增/badcase/{Path(file).name}')

    print(bad_sample)
    print(len(bad_sample))

# FindBadSample()

def CopyandRenameimg():
    save_image = Path('/Users/clustar/Desktop/项目/车牌识别/车牌照片/新增/img1')
    save_image.mkdir(parents=True, exist_ok=True)
    test_file = glob(f'{base_dir}/*/*')
    print(len(test_file))
    for file in test_file:
        if file.endswith('.JPG'):
            shutil.move(file, file.replace('.JPG', '.jpg')) ##将.JPG文件重命名为.jpg
    for file in test_file:
        if file.endswith('.jpg'):
            print(Path(file).parent.name)
            # print(file)
            shutil.copy2(file, f'{save_image}/{Path(file).parent.name}.jpg')
    print(len(glob(f'{save_image}/*')))  #370

# CopyandRenameimg()

def xml2total_text(xml_path):
    if Path(xml_path).exists():
        read_xml = open(xml_path, 'r', encoding='utf8')
        tree = ET.parse(read_xml)
        root = tree.getroot()
        size = root.find('size')
        # 图像宽高
        width = int(size.find('width').text)
        height = int(size.find('height').text)
        # 标注框
        totallist = []
        ob = root.find('object')
        if ob is not None:
            for obj in root.iter('object'):
                bndbox = obj.find('bndbox')
                box = [float(bndbox.find('xmin').text),
                       float(bndbox.find('ymin').text),
                       float(bndbox.find('xmax').text),
                       float(bndbox.find('ymax').text)]
                # 标注越界修正
                if box[2] > width:
                    box[2] = width
                if box[3] > height:
                    box[3] = height
                dict1 = dict()
                dict1["transcription"] = obj.find('name').text.replace('_', '')
                # print(type(obj.find('name').text))
                lefttop = [box[0], box[1]]
                righttop = [box[2], box[1]]
                rightbottom = [box[2], box[3]]
                leftbottom = [box[0], box[3]]
                dict1["points"] = [lefttop, righttop, rightbottom, leftbottom]
                totallist.append(dict1)
            # print(totallist)
            return totallist
        else:
            null_xml_list.append(xml_path)
    else:
        print('标注文件不存在')


def batchxml2txt():
    with open('/Users/clustar/Desktop/项目/车牌识别/车牌照片/新增/data.txt', 'w+') as f:
        xml_file = glob(f'{base_dir}/*/*')
        # print(len(xml_file))
        xml_list = []
        for xml in xml_file:
            if xml.endswith('.xml'):
                # print(Path(xml).parent.name)
                total_list = xml2total_text(xml)
                if total_list is not None:
                    f.writelines(f'img/{Path(xml).parent.name}.jpg' + '\t' + str(total_list) + '\n')
                # xml_list.append(xml)
        for i in sorted(null_xml_list):
            print(Path(i).parent.name)
        print('空标注文件列表数量', len(null_xml_list))
        # print(len(xml_list))

# batchxml2txt()



def splitdata():
    with open('/Users/clustar/Desktop/项目/车牌识别/车牌照片/data总.txt', 'r') as f:
        lines = f.readlines()
        print(len(lines))
        # print(lines)
        ratio = 0.9
        offset = int(len(lines) * ratio)
        train_data = lines[:offset]
        val_data = lines[offset:]

        print(len(train_data))
        print(len(val_data))
        train_image = Path('/Users/clustar/Desktop/项目/车牌识别/车牌照片/licenceplate/train/img')
        train_image.mkdir(parents=True, exist_ok=True)
        test_image = Path('/Users/clustar/Desktop/项目/车牌识别/车牌照片/licenceplate/test/img')
        test_image.mkdir(parents=True, exist_ok=True)

        f1 = open('/Users/clustar/Desktop/项目/车牌识别/车牌照片/licenceplate/train/train.txt', 'w+')
        f2 = open('/Users/clustar/Desktop/项目/车牌识别/车牌照片/licenceplate/test/test.txt', 'w+')
        for i in train_data:
            f1.write(i)
        for j in val_data:
            f2.write(j)
        f1.close()
        f2.close()

        imgdir = Path('/Users/clustar/Desktop/项目/车牌识别/车牌照片/img')
        for train in train_data:
            imgname1 = train.split('\t')[0].split('/')[1]
            print(imgname1)
            shutil.copy2(f'{imgdir}/{imgname1}', f'{train_image}')
        for test in val_data:
            imgname2 = test.split('\t')[0].split('/')[1]
            print(imgname2)
            shutil.copy2(f'{imgdir}/{imgname2}', f'{test_image}')

# splitdata()

def danyinhao2shuangyinhao():
    # with open('/Users/clustar/Desktop/项目/车牌识别/车牌照片/licenceplate/train/train.txt', 'r') as f:
    #     lines = f.readlines()
    #     print(len(lines))
    #     with open('/Users/clustar/Desktop/项目/车牌识别/车牌照片/licenceplate/train/train1.txt', 'w') as f1:
    #         for ln in lines:
    #             f1.write(ln.replace("'", '''"'''))
    #
    # with open('/Users/clustar/Desktop/项目/车牌识别/车牌照片/licenceplate/test/test.txt', 'r') as f:
    #     lines = f.readlines()
    #     print(len(lines))
    #     with open('/Users/clustar/Desktop/项目/车牌识别/车牌照片/licenceplate/test/test1.txt', 'w') as f1:
    #         for ln in lines:
    #             f1.write(ln.replace("'", '''"'''))
    with open('/Users/clustar/Desktop/项目/车牌识别/车牌照片/新增/data.txt', 'r') as f:
        lines = f.readlines()
        print(len(lines)) # 392
        with open('/Users/clustar/Desktop/项目/车牌识别/车牌照片/新增/data1.txt', 'w') as f1:
            for ln in lines:
                f1.write(ln.replace("'", '''"'''))

# danyinhao2shuangyinhao()


def json2total_text(json_path):
    if Path(json_path).exists():
        totallist = []
        with open(json_path, 'r+', encoding='utf8') as fp:
            check_data = json.load(fp)
            if 'shapes' in check_data:
                check_data_list = check_data['shapes']
                for data in check_data_list:
                    dict1 = dict()
                    dict1["transcription"] = str(data['label']).replace('_', '')
                    dict1["points"] = data['points']
                    totallist.append(dict1)
                # print(totallist)
                return totallist
            else:
                null_json_list.append(json_path)
    else:
        print('标注文件不存在')

# json2total_text(jsonfile)



def batchjson2txt(dir):
    with open('/Users/clustar/Desktop/项目/车牌识别/一号车位车牌数据/data.txt', 'w+') as f:
        json_file = glob(f'{dir}/*/*')
        # print(len(xml_file))
        xml_list = []
        for jso in json_file:
            if jso.endswith('.json'):
                # print(Path(xml).parent.name)
                total_list = json2total_text(jso)
                if total_list is not None:
                    f.writelines(f'img/{Path(jso).parent.name}.jpg' + '\t' + str(total_list) + '\n')
                # xml_list.append(xml)
        for i in sorted(null_json_list):
            print(Path(i).parent.name)
        print('空标注文件列表数量', len(null_json_list))

# batchjson2txt()





if __name__ == '__main__':
    base_dir = Path('/Users/clustar/Desktop/项目/车牌识别/一号车位车牌数据/1号车位车牌原始数据')
    null_xml_list = []
    null_json_list = []

    batchjson2txt(base_dir)