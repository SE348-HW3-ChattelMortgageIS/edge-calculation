import serial 
import time 
import string 
import binascii 
import threading 
#定义一个函数： 
def timerDelay(): 
	s=serial.Serial('/dev/ttyUSB0',4800)
	n=s.inWaiting() #采集缓冲数据 
	if n: 
		data= str(binascii.b2a_hex(s.read(n)))[2:-1] 
		l=int(data[6:10],16) #他返还了一堆十六进制数，其中第6到第9表示湿度信息，并将其转换成10进制。 
		l=l/1000 #根据关系计算出湿度信息 
		print('当前湿度为:{:.1%}RH'.format(l)) #输出 
		if data[10]==1: #温度信息 如果这一位为一，证明是负数，需要进行下列操作计算得出温度数值。 
			t=int(data[10:14],16) 
			t=t/10 
			a=bin(t) 
			a=~a 
			b=int(a,2) 
			b=-b 
			print('当前温度为:%.1f℃'%b) 
		else: #如果是正数，则根据如下计算。 
			t=int(data[10:14],16) 
			t=t/10 
			print('当前温度为:%.1f℃'%t) 
		d=bytes.fromhex('000300000002C5DA')
		s.write(d) 
		s.close() 
global q 
q=threading.Timer(2,timerDelay) #进行周期性采集，那个2证明间隔两秒采集一次 
q.start() 
q= threading.Timer(10,timerDelay) #10表示传递一个数据的时间

q.start()
