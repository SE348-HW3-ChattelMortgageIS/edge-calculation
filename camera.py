import cv2
from NumbersGetter import getAccessToken,readImg,sendImg,getMessage
from temprature import init, get_data
import json
import serial
cam = cv2.VideoCapture(10)
import base64
img_counter = 0
import time


#width, height = cam.get(3), cam.get(4)
#print(width, height)

#cam.set(cv2.CAP_PROP_FRAME_WIDTH, width * 2)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height * 2)

#width, height = cam.get(3), cam.get(4)
#print(width, height)

def detail(status, tmp_data, hum_data):
    one = {"identifier":"Data"}
    #two = {"identifier":"Data","value":"{"Temperature":23.4,"status":status,"humidity":34.6"}"}
    #two = {"identifier":"Data","value":"{"Temperature":23.4,"status":"yes","humidity":34.6}"}
    the_str1 = '{"identifier": "Data","value": "{\\"Temperature\\":' + str(hum_data) + ',\\"status\\": \\"'
    the_str2 = status
    the_str3 = '\\",\\"humidity\\":' + str(tmp_data)  + '}"}'
    
    #print (the_str1)
    #print (the_str2)
    #print (the_str3)
    the_str = the_str1+the_str2+the_str3
    print (the_str)
    #str_json=json.loads(the_str)
    #out = json.dumps(one)
    return the_str
    #out = json.dumps(two)
    #return out


ser = init()
flag ='-1'

while cam.isOpened():
    time.sleep(2)
    ret, frame = cam.read()
    if not ret:
        break

    img_name = "/home/pi/photo/opencv_frame_{}.jpg".format(img_counter)
    cv2.imwrite(img_name, frame)
    
    imgbase64 = readImg(img_name)
    resJson = sendImg(imgbase64)
    res,lis = getMessage(resJson)

    f = open('./test_case.json','w')
    #f.truncate()
    if res > 0:
        flag = str(lis[0]%100)
    tmp_data, hum_data = get_data(ser)
    #tmp_data, hum_data = '0', '0'
    out_json = detail(flag, tmp_data, hum_data)
    f.write(out_json)
    f.close()
       


    print("{} written!".format(img_name))
    img_counter += 1

cam.release()
cv2.destroyAllWindows()
