import socket  
import threading,time
class UdpServer:
    def __init__(self):
        self.DeviceList={}
        self.thread_server=threading.Thread(target=self.start)
        self.thread_server.start()
    def start(self):
        address = ('', 48899)  
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.s.bind(address)
        try:
            while True:  
                data, addr = self.s.recvfrom(1024)  
                if not data:  
                    print("exist")
                    break  
                data=str(data)
                d_list=data.replace("b'","").replace("'","").split(',')
                if str(addr[0]) in d_list[0]:
                    temp_device={}
#                    temp_device['IP']=d_list[0]
#                    temp_device['MAC']=d_list[1]
#                    temp_device['SN']=d_list[2]
#                    temp_device['RES']=d_list[3]
                    temp_device['STATUS']=d_list[4]     
                    self.DeviceList[addr[0]]=temp_device
            self.s.close()
        except:
            self.s.close()
            print("Thread Wrong")
    def stop(self):
        self.s.close()
        del self.thread_server
    def getDevice(self):
        return self.DeviceList
    def state(self, IP):
        try:
            ss=UdpServer()
            address = (IP, 48899)  
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
            msg = b"""YZ-RECOSCAN"""
            s.sendto(msg, address)    
            s.close()
            time.sleep(1)
            DeviceList=ss.getDevice()    
            ss.stop()
            for item in DeviceList:
#                print(DeviceList[item])
                print(((str)(DeviceList[item]))[12:13])
        except:
            print("wrong")
        del ss

try:
    ss=UdpServer()
    address = ('192.168.1.106', 48899)  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    msg = b"""YZ-RECOSCAN"""
    s.sendto(msg, address)    
    s.close()
    time.sleep(1)
    DeviceList=ss.getDevice()    
    ss.stop()
    for item in DeviceList:
        print(DeviceList[item])
        print(((str)(DeviceList[item]))[12:13])
except:
    print("wrong")
del ss
