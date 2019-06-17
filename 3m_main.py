#!/usr/bin/env python
import time
#import urllib3
#from time import gmtime, strftime
#from urllib.request import urlopen
#from serial import Serial

import serial
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
phone.write('AT+CIPSEND=80\r')
time.sleep(2)
result = phone.read(100)
print(result)
phone.write('$ANMR,0003,18/24/18-09:35:35,099,0000000819,5EAC7F2E\n#026\r')
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
#while True:
#    temp = 35
#    humi = 80
#    pres = 1015
#    timeQ = strftime("%Y%m%d%H%M%S")
#    url = 'https://api.thingspeak.com/update?api_key=U5B58NFP38B5BTV6&field1='+
str(temp)+'&field2='+str(humi)+'&field3='+str(pres)+'&field4='+timeQ
#    res = urlopen(url).read()
#    print(res)
#    break
 #   time.sleep(10)