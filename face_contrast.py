import requests
import base64
import json
# 1，准备好申请的人脸识别api，API Key， Secret Key
api1= 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Va5yQRHlA4Fq5eR30vV4&client_secret=0rDSjzQ20XUj5itV6WRtznPQSzr5pV'
# api2="https://aip.baidubce.com/rest/2.0/face/v3/match"

# 2,获取token值，拼接API
def get_token():
    response=requests.get(api1)
    access_token=eval(response.text)['access_token']
    api2="https://aip.baidubce.com/rest/2.0/face/v3/match"+"?access_token="+access_token
    return api2

# 3,读取图片数据
def read_img(img1,img2):
    with open(img1,'rb') as f:
        pic1=base64.b64encode(f.read())
    with open(img2,'rb') as f:
        pic2=base64.b64encode(f.read())
    params=json.dumps([
        {"image":str(pic1,"utf-8"),"image_type":'BASE64',"face_type":"LIVE"},
        {"image":str(pic2,"utf-8"),"image_type":'BASE64',"face_type":"IDCARD"}
    ])
    return params

# 4，发起请求拿到对比结果
def analyse_img(file1,file2):
    params=read_img(file1,file2)
    api=get_token()
    content=requests.post(api,params).text
    # print(content)
    score=eval(content)['result']['score']
    if score>80:
        print('图片识别相似度度为'+str(score)+',是同一人')
    else:
        print('图片识别相似度度为'+str(score)+',不是同一人')

analyse_img("/Users/clustar/Desktop/论文/swin例图/1.jpg","/Users/clustar/Desktop/论文/swin例图/2.jpg")

# 打印执行结果：图片识别相似度度为88.23068237,是同一人
# 换图片zly02.jpg和lyf01.jpg：图片识别相似度度为29.28668785,不是同一人
