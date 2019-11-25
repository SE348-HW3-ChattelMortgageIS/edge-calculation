import serial 
import io

ser = serial.Serial("/dev/ttyUSB0", 9600)
ser.write(b'hello')
print("over")

