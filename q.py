import pandas as pd
import numpy as np
np.set_printoptions(threshold=np.inf)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
filename = '/Users/clustar/Desktop/项目/标注数据与陈师傅百分比误差.csv'
info = pd.read_csv(filename)

class_name = ['gjjj','10mm','8mm','6mm','5mm','4mm','3mm','2mm','1_5mm',
            'dbl1','dbl2','dbl3','gj1','gj2','gj3','st1','st2','st3']
sum = 0
sum_list =[]

for name in class_name:
    rows = info[name]
    for row in rows:
        sum = sum + abs(row)
    sum_list.append(sum)
    sum = 0
sort = sorted(sum_list)
print(sum_list)
print(sort[::-1])











