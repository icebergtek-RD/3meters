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

def float_to_hex(f):
	return hex(struct.unpack('<I',struct.pack('<f',f))[0])

def Hash(data):
    #m = int("0xa1b2c3d4",0) #this is m for testing server
    #seed = int("0x1a2b3c4d",0) #this is seed for testing server
    m = int("0x0a9d9c40",0)
    seed = int("0xd5956517",0)
    r = 24
    data=str(data)
    length = len(str(data))
    h = seed ^ length
    currentIndex = 0
    dd = bytes(data, encoding = "utf8")
    ind = 0
    while length >= 4:
        k = dd[ind]
        ind += 1
        k|= (dd[ind] << 8)
        ind += 1
        k|= (dd[ind] << 16)
        ind += 1
        k|= (dd[ind] << 24)
        k = k * m 
        k = k % 4294967296
        k ^= k >> r
        k = k * m
        k = k % 4294967296
        h *= m
        h = h % 4294967296
        h ^= k
        h = h % 4294967296
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

    h ^= (h >> 13)
    h *= m
    h = h % 4294967296
    h ^= (h >> 15)

    return format(h,'X')

def at_command(msg_to_server,server_ip,server_port,idn):
        phone = serial.Serial("/dev/ttyXRUSB1",9600,timeout=5)
        server_ip = bytes(server_ip, encoding = "utf8")
        server_port=bytes(server_port, encoding = "utf8")
        msg_to_server = bytes(str(msg_to_server),encoding="utf8")
        kk = msg_to_server
        slen = len(msg_to_server)
        slen = str(slen)
        slen = bytes(slen,encoding="utf8")
        phone.write(b'AT+NRB\r')
        #print("flag01")
        time.sleep(20)
        phone.write(b'AT+NSOCR=STREAM,6,10005,1,AF_INET\r')
        time.sleep(8)
        #print("flag03")
        result = phone.read(1000)
        print(result)
        #kk=b'$ANMR,2019039999,19/07/26-02:47:55,100,42de38d5,41b1c6a8,42b1c72b,00000000,00000000,00000000,0000$
        slen = len(kk)
        slen = str(slen)
        slen = bytes(slen,encoding="utf8")
        #kk=b'$ANMR,2019039999,19/07/26-02:47:55,100,42de38d5,41b1c6a8,42b1c72b,00000000,00000000,00000000,0000$
        kk=kk.hex()
        kk=bytes(kk,encoding="utf8")
        phone.write(b'AT+NSOCO=1,'+server_ip+b','+server_port+b'\r\n')
        time.sleep(8)
        #print("flag04")
        result = phone.read(1000)
        print(result)
        phone.write(b'AT+NSOSD=1,'+slen+b','+kk+b'\r\n')
        time.sleep(8)
        #print("flag05")
        result = phone.read(1000)
        print(result)
        dresult = result.decode("utf-8")
        if "UPDATE" in dresult:
                ll = dresult.split('[')
                print(ll)
                nip = ll[1]
                nip = nip.split(']')
                nip = nip[0]
                nport = ll[2]
                nport = nport.split(']')
                nport = nport[0]
                fop = open("/home/pi/3meters/config_3m.py","a")
                fop.write("ip='"+nip+"'\n")
                fop.write("port='"+nport+"'\n")
                fop.close()
        fop2 = open("/home/pi/3meters/data.log","a")
        fop2.write(str(msg_to_server)+'\n')
        fop2.write(dresult)
        fop2.close()
        phone.write(b'AT+NSOCL=1\r\n')
        time.sleep(3)
        result = phone.read(1000)
        print(result)
        phone.close

def get_wq(dev,addr):

    client = ModbusClient(method='rtu',port=dev,timeout=1,stopbits=1,bytesize=8,parity='N',baudrate=9600)
    client.connect()
    rr=client.read_input_registers(addr,1,unit=1);
#    print(rr.registers[0]);
    return rr.registers[0]

def work3m():

	### set up for sending message
	msg = "$ANMR,"
	timeQ = strftime("%y/%m/%d-%H:%M:00")
	power = '100'

	### Water Meter Data Reading =========

	#posQf=get_wq('/dev/WQ',107)+get_wq('/dev/WQ',109)/1000
	posQf=88.888
	print(posQf)
	posQ=float_to_hex(posQf)
	posQ=posQ.split('0x')
	posQ=posQ[1]
	#negQf=get_wq('/dev/WQ',111)+get_wq('/dev/WQ',113)/1000
	negQf=33.333
	print(negQf)
	negQ=float_to_hex(negQf)
	negQ=negQ.split('0x')
	negQ=negQ[1]
	totalQf=posQf-negQf
	totalQ=float_to_hex(totalQf)
	totalQ=totalQ.split('0x')
	totalQ=totalQ[1]

	### ==================================

	volt1 = '00000000'
	volt2 = '00000000'
	volt3 = '00000000'
	cur1 = '00000000'
	cur2 = '00000000'
	cur3 = '00000000'
	cWalt = '00000000'
	wLevel = '00000000'

	msg = msg + pid + "," + timeQ + "," + power + ","
	msg = msg + posQ + "," + negQ + "," + totalQ + "," + volt1 + "," + volt2 + "," + volt3 + ","
	msg = msg + cur1 + "," + cur2 + "," + cur3 + "," + cWalt + "," + wLevel
	crc = Hash(msg)
	msg = msg + "," + crc + "\r\n"
	print(msg)
	at_command(msg,ip,port,pid)

os.system("sudo insmod /home/pi/xr/icb/xr_usb_serial_common_lnx-3.6-and-newer-pak/xr_usb_serial_common.ko")
work3m()

#while True:
#	schedule.run_pending()
#	time.sleep(1)
