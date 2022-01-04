import matplotlib.pyplot as plt
import json
import seaborn as sns
import numpy as np
import matplotlib as mpl
import os

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体 SimHei为黑体
mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负
plt.style.use('fivethirtyeight')

"""
    柱状图，对比陈师傅和mask计算出来的百分比
"""


def draw(ch_data, mask_data):
    sns.set_style('darkgrid')
    plt.figure(figsize=(14, 8))
    label = ['gjjj', '10mm', '8mm', '6mm', '5mm', '4mm', '3mm', '2mm', '1_5mm', 'dbl1', 'dbl2', 'dbl3', 'gj1', 'gj2',
             'gj3', 'st1', 'st2', 'st3']

    label_new = ['gjjj','Xmm1','Xmm2','dbl123','gj123','st123']
    label_new_x = [i for i in range(len(label_new))]
    label_new_x1 = [i + 0.2 for i in label_new_x]

    label_x = [i for i in range(len(label))]
    label_x1 = [i + 0.2 for i in label_x]

    chen_y = [ch_data[k] for k in label]
    mask_y = [mask_data[k] for k in label]
    # 占位以免 数据源标签丢失
    y0 = ["" for i in range(len(label))]
    plt.bar(label_x, chen_y, alpha=0.7, width=0.2, color='r', label="chen", tick_label=y0)
    plt.bar(label_x1, mask_y, alpha=0.7, width=0.2, color='b', label="mask", tick_label=label)
    # 给图加text
    for x, y in zip(label_x, chen_y):
        plt.text(x, y + 0.05, '%.2f' % y, ha='center', va='bottom', fontsize='7')
    for x, y in zip(label_x1, mask_y):
        plt.text(x + 0.2, y + 0.05, '%.2f' % y, ha='center', va='bottom', fontsize='7')
    plt.ylim(0, +100)
    # plt.xlabel("料件类型", color='r')  # X轴标签
    # plt.ylabel("所占比重", color='r')  # Y轴标签
    plt.grid(True)
    plt.legend()  # 显示图例
    title = str(mask_data['date']) + '-' + mask_data['car_num']
    plt.title(title)  # 图标题
    plt.legend()
    os.makedirs('data/charts',exist_ok=True)
    img_path = os.path.join('data/charts',title+'.jpg')
    plt.savefig(img_path)
    # plt.show()
    plt.close()


if __name__ == '__main__':
    with open('result.json','r',encoding='utf8') as fp:
        check_data = json.load(fp)
    for item in check_data:
        print(item)
        ch_data = item['chen']
        mask_data = item['mask']
        date = ch_data['date']
        car_num = ch_data['car_num']
        # if car_num=='CAW0790' and date == 20210113:
        draw(ch_data,mask_data)






# 20210113_CAW0790 0.3606
# 20201207_LQ616FC 0.4008
# 20210113_GN60693 0.4028
# 20201207_GN29081 0.4036
# 20210116_GK29199 0.4096
# 20210113_CAAT010 0.4219
# 20210126_CT51283 0.4223
# 20210114_GJ87303 0.4244
# 20210116_CR80076 0.4251
# 20210115_CAAP667 0.4291
# 20201209_CAQ8295 0.4294

