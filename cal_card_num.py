from glob import glob

date_num = 0
car_total = 0
image_total = 0
base_path = '/home/centos/smb/jsl/图片数据'
# base_path = '/Users/clustar/Desktop/项目/data0'
# f = open('/Users/clustar/Desktop/项目/data_describe.txt', 'w')
f = open('/home/centos/zhaoliang/data_statistics.txt', 'w')
date_list = glob(f'{base_path}/*')
date_set = [date.split('/')[-1] for date in date_list]
date_set = sorted(date_set)
for date_ in date_set:
    if date_.isdigit():
        date_num += 1
print(f'当前共有 {date_num} 天的数据')

for i in range(len(date_set)):
    car_list = glob(f'{base_path}/{date_set[i]}/*')
    car_set = [car.split('/')[-1] for car in car_list]
    if car_set:
       print(f'{date_set[i]}有 {len(car_set)} 车，车牌号是：{car_set}')
       f.write(f'{date_set[i]}有 {len(car_set)} 车，车牌号是：{car_set}'+'\n')
    car_total = car_total + len(car_set)
print(f'目前总共有 {car_total} 车次')

image_list = glob(f'{base_path}/*/*/*')
for image in image_list:
    if image.endswith('jpg'):
       image_total += 1

print(f'当前数据集共有图片 {image_total} 张')

