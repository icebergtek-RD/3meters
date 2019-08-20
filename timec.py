#!/usr/bin/env python3

import time
from time import gmtime, strftime
import os
import ctypes as ct
import serial
import schedule
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import sys
import struct
import binascii
sys.path.append("/home/pi/3meters")
from config_3m import *

phone = serial.Serial("/dev/ttyXRUSB1",9600,timeout=5)
phone.write(b'AT+CCLK?\r')
time.sleep(10)
result = phone.read(100)
print(result)
result=str(result)
if "OK" in result:
  ll=result.split(':')
  ll2=ll[1].split(',')
  dt='20'+ll2[0]
  hh=ll2[1]
  mm=ll[2]
  tt=dt+' '+hh+':'+mm+':00GMT'
print(tt)

os.system("sudo date -s \""+tt+"\"")
