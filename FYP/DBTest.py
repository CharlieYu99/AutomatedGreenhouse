#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import datetime
import ADS1256
import DAC8532
import RPi.GPIO as GPIO
import pymysql

#conn=pymysql.connect('10.7.143.64','Greenhouseadmin','adminpassword')
#conn=pymysql.connect(host='localhost',
#                             port=3306,
#                             user='Greenhouseadmin',
#                             password='adminpassword',
#                             db='GreenhouseDB',
#                             charset='utf8')
#conn.select_db('GreenhouseDB')
#cur=conn.cursor()

# sql = """INSERT INTO test_table (time,light_level,plug_state) VALUES (%s, %s, %s);"""
# val = (datetime.datetime.now(),11111,True)
# #sql = """INSERT INTO test_table (time,light_level) VALUES ("2021-03-04 14:07:58.423854",0.386124);"""
# cur.execute(sql,val)
# conn.commit()


    
try:
    ADC = ADS1256.ADS1256()
    DAC = DAC8532.DAC8532()
    ADC.ADS1256_init()

    DAC.DAC8532_Out_Voltage(0x30, 3)
    DAC.DAC8532_Out_Voltage(0x34, 3)
    while(1):
        ADC_Value = ADC.ADS1256_GetAll()
        print ("0 ADC = %lf"%(ADC_Value[0]*5.0/0x7fffff))
        #print ("1 ADC = %lf"%(ADC_Value[1]*5.0/0x7fffff))
        #print ("2 ADC = %lf"%(ADC_Value[2]*5.0/0x7fffff))
        #print ("3 ADC = %lf"%(ADC_Value[3]*5.0/0x7fffff))
        print ("4 ADC = %lf"%(ADC_Value[4]*5.0))
        print ("5 ADC = %lf"%(ADC_Value[5]*5.0))
        #print ("6 ADC = %lf"%(ADC_Value[6]*5.0/0x7fffff))
        #print ("7 ADC = %lf"%(ADC_Value[7]*5.0/0x7fffff))
        
        #temp = (ADC_Value[0]>>7)*5.0/0xffff
        #print ("DAC :",temp)
        #print ("\33[10A")
        #DAC.DAC8532_Out_Voltage(DAC8532.channel_A, temp)
        #DAC.DAC8532_Out_Voltage(DAC8532.channel_B, 3.3 - temp)
        
        #sql = """INSERT INTO test_table (time,light_level) VALUES (%s, %s);"""
        #val = (datetime.datetime.now(),ADC_Value[0]*5.0/0x7fffff)
        #sql = """INSERT INTO test_table (time,light_level) VALUES ("2021-03-04 14:07:58.423854",0.386124);"""
        #cur.execute(sql,val)
        #conn.commit()
        
        time.sleep(1)

except :
    GPIO.cleanup()
    print ("\r\nProgram end")
    exit()
