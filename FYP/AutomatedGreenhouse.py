# some base libraries
import RPi.GPIO as GPIO
import time
import datetime
import os
import threading
import pandas as pd

# sensor libraries
import Adafruit_DHT
import ADS1256
# import DAC8532

# smart plug libraries
from smartplug import SmartPlug
import Reco4lifeP10A as Reco

# database library
import pymysql

# sunrise sunset calculate
from sunrise_sunset import SunriseSunset

# GPIO setting
GPIO.setmode(GPIO.BCM)

# 102,103 Edimax
# 104,105,106,107,108 Reco

# device_setting
Humidifier_setting = ("192.168.0.103", "Edimax")
Heater_setting = ("192.168.0.102", "Edimax")
Fan0_setting = ("192.168.0.106", "Reco4life")
Fan1_setting = ("192.168.0.105", "Reco4life")
Pump_setting = ("192.168.0.107", "Reco4life")
Light0_setting = ("192.168.0.104", "Reco4life")
# Light1_setting = ("192.168.0.108","Reco4life")
DHT22_pin_in = 18
DHT22_pin_out = 3

# value limits
# light_limit_low = 2000000
# light_limit_high = 200000
# temperature_limit_low = 20
# temperature_limit_high = 28
# humidity_limit_low = 40
# humidity_limit_high = 99
# moisture_limit_low = 2000000

watering_warranty = -1
auto_watering_time = 4 #days

# collection period
collection_frequency = 60*30

# program setting
print_val = True

# geography position (Suzhou for the below setting)
longitude = 120.62
latitude = 31.32
timezone_offset = 8

# private class for smart plugs control (combine into one object)
class Device:
    def __init__(self, ip, type, name):
        self._IP = ip
        self._type = type
        self._name = name

    def on(self):
        if self._type == "Edimax":
            SmartPlug(self._IP, ('admin', 'password')).state = 'ON'
        elif self._type == "Reco4life":
            Reco.on(self._IP)

    def off(self):
        if self._type == "Edimax":
            SmartPlug(self._IP, ('admin', 'password')).state = 'OFF'
        elif self._type == "Reco4life":
            Reco.off(self._IP)

    def name(self):
        return self._name

# Device inits
Humidifier = Device(Humidifier_setting[0], Humidifier_setting[1], "humidifier")
Heater = Device(Heater_setting[0], Heater_setting[1], "heater")
Fan0 = Device(Fan0_setting[0], Fan0_setting[1], "fan0")
Fan1 = Device(Fan1_setting[0], Fan1_setting[1], "fan1")
Pump = Device(Pump_setting[0], Pump_setting[1], "waterpump")
Light0 = Device(Light0_setting[0], Light0_setting[1], "light")
# Light1 = Device(Light1_setting[0], Light1_setting[1], "light1")

# device list for control in a whole
device_list = []
device_list.append(Humidifier)
device_list.append(Heater)
device_list.append(Fan0)
device_list.append(Fan1)
device_list.append(Pump)
device_list.append(Light0)
# device_list.append(Light1)

# init the device state
light_state = False
waterpump_state = False
humidifier_state = False
heater_state = False
fan0_state = False
fan1_state = False

ADC = ADS1256.ADS1256()
ADC.ADS1256_init()


def trigger():
    while(True):
        thread = threading.Thread(target=data_collection_and_storage)
        thread.start()
        time.sleep(collection_frequency)


def data_collection_and_storage():
        # data collection
        # AD-DA module
        try:
            ADC_Value = ADC.ADS1256_GetAll()
            light_0 = int(ADC_Value[0])
            light_1 = int(ADC_Value[1])
            CO2_0 = int(ADC_Value[2])
            CO2_1 = int(ADC_Value[3])
            moisture_0 = int(ADC_Value[4])
            moisture_1 = int(ADC_Value[5])
            moisture_2 = int(ADC_Value[6])
            moisture_3 = int(ADC_Value[7])
        except :
            GPIO.cleanup()
            print ("AD module interrupted")
            # exit()

        time.sleep(2)
        # DHT22
        DHT22 = Adafruit_DHT.DHT22
        humidity22_in, temperature22_in = Adafruit_DHT.read_retry(DHT22, DHT22_pin_in)
        try:
            humidity22_in = int(humidity22_in)
            temperature22_in = int(temperature22_in)
        except:
            print ("DHT22 read failure")
            humidity22_in = 0
            temperature22_in = 0

        time.sleep(2)

        humidity22_out, temperature22_out = Adafruit_DHT.read_retry(DHT22, DHT22_pin_out)
        try:
            humidity22_out = int(humidity22_out)
            temperature22_out = int(temperature22_out)
        except:
            print ("DHT22 read failure")
            humidity22_out = 0
            temperature22_out = 0

        humidity22_in = humidity22_in if humidity22_in <= 100 and humidity22_in > 0 else 0
        temperature22_in = temperature22_in if humidity22_in <= 100 and humidity22_in > 0 else 0
        humidity22_out = humidity22_out if humidity22_out <= 100 and humidity22_out > 0 else 0
        temperature22_out = temperature22_out if humidity22_out <= 100 and humidity22_out > 0 else 0

        if print_val:
            print ("light_0: %i, light_1: %i"%(ADC_Value[0],ADC_Value[1]))
            print ("CO2_0: %i, CO2_1: %i"%(ADC_Value[2],ADC_Value[3]))
            print ("moisture_0: %i, moisture_1: %i, moisture_2: %i, moisture_3: %i"%(ADC_Value[4],ADC_Value[5],ADC_Value[6],ADC_Value[7]))
            if (humidity22_in == 0 and temperature22_in == 0):
                print("DHT22 inside failure")
            else:
                print("DHT22 inside: humidity = %i, temperature = %i" % (humidity22_in, temperature22_in))
            if (humidity22_out == 0 and temperature22_out == 0):
                print("DHT22 outside failure")
            else:
                print("DHT22 outside: humidity = %i, temperature = %i" % (humidity22_out, temperature22_out))
                
        device_control(ADC_Value,temperature22_in,humidity22_in,temperature22_out,humidity22_out)

        # database storage
        conn=pymysql.connect(host='localhost',
                             port=3306,
                             user='Greenhouseadmin',
                             password='adminpassword',
                             db='GreenhouseDB',
                             charset='utf8')
        cur=conn.cursor()
        sql = """INSERT INTO environment_status ( time,
                                    sensor_light_0,sensor_light_1,
                                    sensor_CO2_0,sensor_CO2_1,
                                    sensor_moisture_0,sensor_moisture_1,sensor_moisture_2,sensor_moisture_3,
                                    sensor_temperature_inside,sensor_humidity_inside,
                                    sensor_temperature_outside,sensor_humidity_outside,
                                    device_light,
                                    device_waterpump,
                                    device_fan_0,device_fan_1,
                                    device_humidifier,
                                    device_heater) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        val = ( datetime.datetime.now(),
                light_0, light_1, 
                CO2_0, CO2_1, 
                moisture_0, moisture_1, moisture_2, moisture_3, 
                temperature22_in, humidity22_in,
                temperature22_out, humidity22_out,
                light_state, 
                waterpump_state, 
                fan0_state, fan1_state, 
                humidifier_state,
                heater_state)
        cur.execute(sql,val)
        conn.commit()
        cur.close()
        conn.close()

        


def device_control(ADC_Value,temperature22_in,humidity22_in,temperature22_out,humidity22_out):
    global light_state, waterpump_state, humidifier_state, heater_state, fan0_state, fan1_state, watering_warranty

    light_0 = int(ADC_Value[0])
    light_1 = int(ADC_Value[1])
    CO2_0 = int(ADC_Value[2])
    CO2_1 = int(ADC_Value[3])
    moisture_0 = int(ADC_Value[4])
    moisture_1 = int(ADC_Value[5])
    moisture_2 = int(ADC_Value[6])
    moisture_3 = int(ADC_Value[7])

    light_limit_low, light_limit_high, temperature_limit_low, temperature_limit_high, humidity_limit_low, humidity_limit_high, moisture_limit_low = get_device_limit()
    

    # Light
    # calculate the time for sunrise and sunset
    ro = SunriseSunset(datetime.datetime.now(), latitude=latitude, longitude=longitude, localOffset=timezone_offset)
    rise_time, set_time = ro.calculate()
    rise_time = rise_time.strftime("%H:%M:%S")
    set_time = set_time.strftime("%H:%M:%S")
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    
    if time_now > rise_time and time_now < set_time:
        if light_0 > light_limit_low and not light_state:
            Light0.on()
            light_state = True
        elif light_0 <= light_limit_low and light_state:
            Light0.off()
            light_state = False
    else:
        Light0.off()
        light_state = False

    # Temperature

    if temperature22_in < temperature_limit_low and temperature22_in != 0:
        # if the temperature is low, turn on the heater and the fan to warm the greenhouse
        fan0_state = True
        fan1_state = True
        heater_state = True

        Fan0.on()
        Fan1.on()
        device_control_single(Heater,collection_frequency,60,120)

    elif temperature22_in > temperature_limit_high and temperature22_in != 0:
        # if the temperature is high, turn on the fan to circulate the air to cool the greenhouse down. at the same time, turn on the humidifier to accelerate the cooling 
        fan0_state = True
        fan1_state = True
        humidifier_state = True

        Fan0.on()
        Fan1.on()
        device_control_single(Humidifier,collection_frequency,30,90)

    else:
        fan0_state = False
        fan1_state = True
        humidifier_state = False
        heater_state = False
        Fan0.off()
        Fan1.on()


    # humidity
    if humidity22_in < humidity_limit_low and humidity22_in != 0 and not humidifier_state:
        humidifier_state = True
        device_control_single(Humidifier,collection_frequency,15,105)

    # moisture
    if ((((moisture_0 + moisture_1 + moisture_2 + moisture_3) / 4) > moisture_limit_low) and watering_warranty > 24*(60*60 / collection_frequency)):
        Pump.on()
        waterpump_state = True
        time.sleep(10)
        Pump.off()
        watering_warranty = 0
    elif watering_warranty >= auto_watering_time * 24 * (60*60 / collection_frequency):
        Pump.on()
        waterpump_state = True
        time.sleep(10)
        Pump.off()
        watering_warranty = 0
    else:
        waterpump_state = False
        watering_warranty += 1


# helper function for device control
def device_control_single(device, duration, on_time, off_time):
    t = threading.Thread(target=device_control_helper,args=(device,duration,on_time,off_time))
    t.start()


def device_control_helper(device, duration, on_time, off_time):
    for i in range(int(duration/ (on_time + off_time))):
        if (not(device_in_control(device))):
            device.on()
        time.sleep(on_time)
        if (not(device_in_control(device))):
            device.off()
        time.sleep(off_time)

def device_in_control(device):
    dbconn=pymysql.connect(
    host="localhost",
    database="GreenhouseDB",
    user="Greenhouseadmin",
    password="adminpassword",
    port=3306,
    charset='utf8'
    )
    device_name = device.name()
    sqlcmd = "SELECT " + device_name + " FROM GreenhouseDB.user_control where " + device_name + " is not null order by id desc;"
    df=pd.read_sql(sqlcmd,dbconn)
    in_control = df.to_dict("list")[device_name][0] == True
    return in_control

def get_device_limit():
    dbconn=pymysql.connect(
    host="localhost",
    database="GreenhouseDB",
    user="Greenhouseadmin",
    password="adminpassword",
    port=3306,
    charset='utf8'
    )

    light_limit_low = get_device_limit_helper(dbconn,"light_limit_low")
    light_limit_high = get_device_limit_helper(dbconn,"light_limit_high")
    temperature_limit_low = get_device_limit_helper(dbconn,"temperature_limit_low")
    temperature_limit_high = get_device_limit_helper(dbconn,"temperature_limit_high")
    humidity_limit_low = get_device_limit_helper(dbconn,"humidity_limit_low")
    humidity_limit_high = get_device_limit_helper(dbconn,"humidity_limit_high")
    moisture_limit_low = get_device_limit_helper(dbconn,"moisture_limit_low")

    return (light_limit_low, light_limit_high, temperature_limit_low, temperature_limit_high, humidity_limit_low, humidity_limit_high, moisture_limit_low)

def get_device_limit_helper(dbconn,key):
    sqlcmd = "SELECT " + key + " FROM GreenhouseDB.user_settings where " + key + " is not null order by id desc;"
    df=pd.read_sql(sqlcmd,dbconn)
    return df.to_dict("list")[key][0]

if __name__ == '__main__':
    try:
        trigger()
    except KeyboardInterrupt:
        for device in device_list:
            device.off()
        pass
