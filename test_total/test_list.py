# label = ['gjjj', '10mm', '8mm', '6mm', '5mm', '4mm', '3mm', '2mm', '1_5mm', 'dbl1', 'dbl2', 'dbl3', 'gj1', 'gj2',
#          'gj3', 'st1', 'st2', 'st3']
#
# label_1 = ['10mm', '8mm', '6mm', '5mm', '4mm', '3mm', '2mm', '1_5mm']
# label_2 = ['dbl1', 'dbl2', 'dbl3']
# label_3 = ['gj1', 'gj2', 'gj3']
# label_4 = ['st1', 'st2', 'st3']
#
# # for k in label_1:
# #     if k in label:
# #         print(k)
# #
# # for k in label_2:
# #     if k in label:
# #         print(k)
# #
# # for k in label_3:
# #     if k in label:
# #         print(k)
# #
# # for k in label_4:
# #     if k in label:
# #         print(k)
#
#
# a = [1, 2, 3, 4]
# b = [1, 2, 3, 4]
#
# print(type(a))
# print(str(a))

import os

str1 = '/home/zhaoliang/PaddleOCR/test/chegnshi_1cp_20211207033252_5795366.jpg'
str2 = '/home/zhaoliang/PaddleOCR/test/chegnshi_1cp_20211213200820_4408531.jpg'

x = os.path.splitext(str2)[-1][1:]
print(x)



