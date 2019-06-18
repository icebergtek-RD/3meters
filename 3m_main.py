#!/usr/bin/env python
import time
#import urllib3
from time import gmtime, strftime
#from urllib.request import urlopen
#from serial import Serial

import ctypes as ct
import serial
#from pymodbus.client.sync import ModbusSerialClient as ModbusClient


def Hash(data):
#    data = ct.c_uint16(data)
    m = int("0xa1b2c3d4",0)
    seed = int("0x1a2b3c4d",0)
    r = 24
    data=str(data)
    length = len(str(data))
    h = seed ^ length
#    h = ct.c_uint16(h)
    currentIndex = 0
    dd = bytes(data, encoding = "utf8")
    ind = 0
    while length >= 4:
        k = dd[ind]
#        print("1--k="+str(k))
        ind += 1
        k|= (dd[ind] << 8)
#        print("2--k="+str(k))
        ind += 1
        k|= (dd[ind] << 16)
#        print("3--k="+str(k)) 
        ind += 1
        k|= (dd[ind] << 24)
#        print("4--k="+str(k))  
#        print("m="+str(m)+",length="+str(length)+",h="+str(h))  
        k = k * m 
        k = k % 4294967296
#        print("m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))  
        k ^= k >> r
#        print("m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))  
        k = k * m
        k = k % 4294967296
#        print("m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))  
        h *= m
        h = h % 4294967296
#        print("m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))  
        h ^= k
        h = h % 4294967296
#        print("m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))
        ind += 1  
        length -= 4
    
    if length == 3:
        k = dd[ind+0]
        k |= (dd[ind+1] << 8)
        h ^= k
        h ^= (dd[ind+2] << 16)
        h *= m
        h = h % 4294967296

    if length == 2:
        k = dd[ind+0]
        k |= (dd[ind+1] << 8)
        h ^= k
        h *= m
        h = h % 4294967296

    if length == 1:
        k = dd[ind+0]
        h ^= k
        h *= m
        h = h % 4294967296
#        print("case1: m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))  

    h ^= (h >> 13)
    h *= m
    h = h % 4294967296
    h ^= (h >> 15)
#    print("m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))  

    return format(h,'X')


#print(str(Hash("$ANMR,0912000000,19/06/12-16:14:00,100,00000000,00000000,00000000,436F3720,4386D1EE,437C0C3D,42A26FF6,42A61BCC,429D550A,48339980,00000000")) )   

def at_command(msg_to_server,server_ip,server_port):
	phone = serial.Serial("/dev/ttyUSB3",119200,timeout=5,rtscts=True,dsrdtr=True)
	phone.write('AT+CSTT="twm.nbiot"\r')
	time.sleep(0.5)
	result = phone.read(1000)
	print(result)
	phone.write('AT+CGATT?\r')
	time.sleep(0.5)
	result = phone.read(1000)
	print(result)
	phone.write('AT+CIICR\r')
	time.sleep(0.5)
	result = phone.read(1000)
	print(result)
	phone.write('AT+CIFSR\r')
	time.sleep(0.5)
	result = phone.read(1000)
	print(result)
	phone.write('AT+CIPSTART="TCP","220.133.128.61","48877"\r')
	#phone.write('AT+CIPSEND\r')
	#phone.write('$ANMR,0003,18/24/18-09:35:35,099,0000000819,5EAC7F2E\r')
	time.sleep(0.5)
	result = phone.read(100)
	print(result)
	#phone.write('AT+CIPSEND=0,80\r')
	#time.sleep(2)
	#result = phone.read(100)
	phone.write('AT+CIPSEND=150\r')
	time.sleep(2)
	result = phone.read(100)
	print(result)
	msg_to_server = msg_to_server + '\n#026\r'
	phone.write(msg_to_server)
	#phone.write(0x1a)
	time.sleep(10)
	result = phone.read(1000)
	print(result)
	#phone.write('AT+CIPPING="8.8.8.8"')
	#result = phone.read(1000)
	#print(result)
	phone.write('AT+CIPCLOSE\r')
	time.sleep(3)
	result = phone.read(1000)
	print(result)
	phone.write('AT+CIPSHUT\r')
	time.sleep(3)
	result = phone.read(1000)
	print(result)
	phone.close

def get_wq(dev,addr):

    client = ModbusClient(method='rtu',port=dev,timeout=1,stopbits=1,bytesize=8,parity='N',baudrate=9600)
    client.connect()
    rr=client.read_input_registers(addr,1,unit=1);
    print(rr.registers[0]);

### set up for sending data
ip = "220.133.128.61"
port = "48877"

### set up for sending message
msg = "$ANMR,"
pid = "2019030001"
timeQ = strftime("%d/%m/%Y-%H:%M:%S")
power = '100'
posQ = '00000000'
negQ = '00000000'
totalQ = '00000000'
volt1 = '00000000'
volt2 = '00000000'
volt3 = '00000000'
cur1 = '00000000'
cur2 = '00000000'
cur3 = '00000000'
cWalt = '00000000'
wLevel = '00000000'

msg = msg + pid + "," + timeQ + "," + power + "," + timeQ + "," + power + ","
msg = msg + posQ + "," + negQ + "," + totalQ + "," + volt1 + "," + volt2 + "," + volt3 + ","
msg = msg + cur1 + "," + cur2 + "," + cur3 + "," + cWalt + "," + wLevel
crc = Hash(msg)
msg = msg + "," + crc
print(msg)


#while True:
#    temp = 35
#    humi = 80
#    pres = 1015
#    timeQ = strftime("%Y%m%d%H%M%S")
#    url = 'https://api.thingspeak.com/update?api_key=U5B58NFP38B5BTV6&field1='+str(temp)+'&field2='+str(humi)+'&field3='+str(pres)+'&field4='+timeQ
#    res = urlopen(url).read()
#    print(res)
#    break
 #   time.sleep(10)