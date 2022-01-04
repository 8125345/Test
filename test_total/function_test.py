import json
# a = max(2919, 3523)
# print(a)

# a = [2919, 3523]
#
# print(a)
# b = []
#
# b.append(a)
#
# f = open('./coor.txt','w')
# f.write(json.dumps(a)+'\n')
#
# print(b)

# f = open('./coor.txt','r')
#
# for line in f.readlines():
#     print(line)
#     print(type(line))

import mmcv
import numpy as np


"""
一、从已有的数据结构里转成numpy
"""
lst2 = [(3.14, 2.17, 0, 1, 2), (1, 2, 3, 4, 5)]
nd2 = np.array(lst2)
# print(nd2)


"""
二、 随机初始化numpy
"""
nd3 = np.random.random([3, 3]) #生成3*3大小的在0～1之间的随机数
# print(nd3)

nd4 = np.random.uniform(10, 20, 2) #生成在区间[10, 20)的两个均匀分布的随机数
# print(nd4)

nd5 = np.random.randn(20) #生成20个满足标准正态分布的随机数
# print(nd5)

nd6 = np.random.randint(1, 20, (1, 3)) #生成[1, 20)的6个整数
# print(nd6)

nd7 = np.random.normal(20, 0.2, 9) #生成均值为20，scale为0.2 ，9个数
# print(nd7)

np.random.seed(123)
nd8 = np.random.randn(2, 3)
# print(nd8)
np.random.seed(123)
nd9 = np.random.randn(2, 3)
# print(nd9)


nd10 = np.eye(3, 4)
# print(nd10)
# print(nd10.reshape((2, 6)))
# print(nd10.reshape(2, 6))
# print(nd10.reshape([2, 6]))


"""
三、 数组变形
"""
arr = np.arange(10)
# print(arr.reshape(2, 5))
# print(arr.reshape(2, 5).T)


"""
四、 数组合并
"""
a = np.arange(4).reshape(2, 2)
b = np.arange(4).reshape(2, 2)
# print(a)
# print(b)
# print(np.append(a, b))
# print(np.append(a, b, axis=0)) #按行合并
# print(np.append(a, b, axis=1)) #按列合并
# print(np.vstack(a, b))


import torch
from torch.nn import functional as F

x_half = torch.Tensor([1 / 0.5, 2 / 0.5, 3 / 0.5])
p_half = F.softmax(x_half, dim=0)
print('T=0.5,softmax输出', p_half)

x1 = torch.Tensor([1, 2, 3])
p1 = F.softmax(x1, dim=0)
print('T=1,softmax输出', p1)

x_2 = torch.Tensor([1 / 2, 2 / 2, 3 / 2])
p_2 = F.softmax(x_2, dim=0)
print('T=2,softmax输出', p_2)

x_4 = torch.Tensor([1 / 4, 2 / 4, 3 / 4])
p_4 = F.softmax(x_4, dim=0)
print('T=4,softmax输出', p_4)






