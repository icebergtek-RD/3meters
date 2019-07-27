#!/usr/bin/env python
import time
#import urllib3
#from time import gmtime, strftime
#from urllib.request import urlopen
#from serial import Serial
import os
#import ctypes as ct
import serial
#import schedule
#from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import sys
#import struct
#import binascii


#with open("/dev/pts/1","wb+",buffering=0) as term:
#  term.write("AT+CSQ\r\n".encode())
#  while True:
#    print(term.read(1).decode(),end='')
#    sys.stdout.flush()


phone = serial.Serial("/dev/ttyXRUSB1",9600,timeout=5)
#phone.write(serialcmd.encode('AT'))
phone.write(b'AT+NRB\r')
print("flag01")
time.sleep(20)
#qq=b'AT+CSQ\r\n'
#qq='1'
#qq=str.encode('AT+CSQ\r\n')
phone.write(b'AT+NSOCR=STREAM,6,10005,1,AF_INET\r')
#print(qq)
#phone.write(qq)
#print("flag02")
time.sleep(8)
print("flag03")
result = phone.read(1000)
print(result)
kk=b'$ANMR,2019039999,19/07/26-02:47:55,100,42de38d5,41b1c6a8,42b1c72b,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,AC4E4F1E'
slen = len(kk)
slen = str(slen)
slen = bytes(slen,encoding="utf8")
kk=b'$ANMR,2019039999,19/07/26-02:47:55,100,42de38d5,41b1c6a8,42b1c72b,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,AC4E4F1E'
#kk=kk.encode("utf-8")
#kk=
#kk=bytes(kk,encoding="utf8")
kk=kk.hex()
kk=bytes(kk,encoding="utf8")
phone.write(b'AT+NSOCO=1,220.133.128.61,50001\r\n')
time.sleep(8)
print("flag04")
result = phone.read(1000)
print(result)

phone.write(b'AT+NSOSD=1,'+slen+b','+kk+b'\r\n')
#phone.write(b'AT+NSOSD=1,2,AB30\r\n')
time.sleep(8)
print("flag05")
result = phone.read(1000)
print(result)

phone.write(b'AT+NSOCL=1\r')
time.sleep(3)
result = phone.read(1000)
print(result)
phone.close()
