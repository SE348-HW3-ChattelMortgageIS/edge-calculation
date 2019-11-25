# -*- coding:utf-8 -*-
# Author: WUJiang
# 运行环境为Ubuntu14.04&Python2.7

import serial
import time



def init():
	ser = serial.Serial("/dev/ttyUSB0", 9600) # 选择串口，并设置波特率
	return ser 

def get_data(ser):
	if ser.is_open:
		# hex(16进制)转换为bytes(2进制)，应注意Python2.7与Python3.7此处转换的不同
		send_data = '010300000002C40B'
		send_data = bytes.fromhex(send_data)    # 发送数据转换为b'\xff\x01\x00U\x00\x00V'
		ser.write(send_data)   # 发送命令
		time.sleep(0.1)        # 延时，否则len_return_data将返回0，此处易忽视！！！
		len_return_data = ser.inWaiting()  # 获取缓冲数据（接收数据）长度
		if len_return_data:
			return_data = ser.read(len_return_data)  # 读取缓冲数据
		# bytes(2进制)转换为hex(16进制)，应注意Python2.7与Python3.7此处转换的不同，并转为字符串后截取所需数据字段，再转为10进制
			str_return_data = return_data.hex()
			feedback_data = int(str_return_data, 16)
			tmp_data = int(str_return_data[7:10], 16)/10
			hum_data = int(str_return_data[11:14], 16)/10
			print(tmp_data)
			print(hum_data)
			return tmp_data, hum_data
	else:
		print("port open failed")
		return '0', '0'

