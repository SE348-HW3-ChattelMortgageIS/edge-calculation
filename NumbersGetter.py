# 本文件为读取图片信息并上传baidu api获取其中数字信息的python程序
# api的局限性：
#	1. 图片应较为清晰光亮充足
#	2. 图片最好为单据数据（文档中使用的例子为快递单，收据等，明显这类数据准确度更高）
#	3. 图片中数字打印识别效果远高于手写识别效果，尽可能使用打印数字作为识别对象
#	4. 每日免费次数为200
import requests
import base64
import json

# 百度接口调用的配置
def getAccessToken():
    appkey = "LZ7XNWWV8XeKN0XsE94PoOzt"
    secretkey = "T5H3C7ZoClU8FRzzSnIAM6Z9GdmUAQBG"
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+ appkey + '&client_secret=' + secretkey
    response = requests.get(host)
    if response:
        return response.json()['access_token']
    else:
        print("未得到access token")
        return

# 读取图片并使用base64编码
def readImg(path):
    img = open(path, "rb")
    imgBase64 = base64.b64encode(img.read())
    img.close()
    return imgBase64

# 将数据发送至baidu api并获得json
def sendImg(imgBase64Code):
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/numbers?access_token='+getAccessToken()
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
    }
    body = {
        "image": imgBase64Code,
    }
    response = requests.post(url, body, headers = headers)
    return response.text

# 解析json数据并提取其中的数字个数和数字数组
def getMessage(numberJson):
    message = json.loads(numberJson)
    resultNum = message.get('words_result_num')
    resultList = message.get('words_result')
    for i in range(len(resultList)):
        resultList[i] = resultList[i]['words']
    return resultNum, resultList

# 更新path以获得图片数据
#path = "./1.png"
#resJson = sendImg(readImg(path))
#res, lis = getMessage(resJson)
#print("内部数字字符", lis)
