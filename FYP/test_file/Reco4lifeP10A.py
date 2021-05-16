from socket import *
import threading
import time
import datetime

import search

def on(IP):
    HOST=IP
    PORT=8899
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect((HOST,PORT))
    data2 =b"""AT+YZSWITCH=1,ON,time"""
    tcpCliSock.send(data2)
    data1 = tcpCliSock.recv(1024)
    print (data1)
    
def off(IP):
    HOST=IP
    PORT=8899
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect((HOST,PORT))
    data2 =b"""AT+YZSWITCH=1,OFF,time"""
    tcpCliSock.send(data2)
    data1 = tcpCliSock.recv(1024)
    print (data1)
    
def state(IP):
    try:
        ss=search.UdpServer()
        address = (IP, 48899)  
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        msg = b"""YZ-RECOSCAN"""
        s.sendto(msg, address)    
        s.close()
        time.sleep(1)
        DeviceList=ss.getDevice()    
        ss.stop()
        for item in DeviceList:
#               print(DeviceList[item])
             print(((str)(DeviceList[item]))[12:13])
    except:
        print("wrong")
    del ss

if __name__ == '__main__':
    print (datetime.datetime.now())
    ip1 = '192.168.1.107'
    ip2 = '192.168.1.106'
    on(ip1)
    state(ip1)
    time.sleep(2)
    off(ip1)
#    state(ip2)
    