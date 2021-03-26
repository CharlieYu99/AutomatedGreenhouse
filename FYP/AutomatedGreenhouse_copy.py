# some base libraries
import RPi.GPIO as GPIO
import time
import datetime
import os
import threading

# sensor libraries
import Adafruit_DHT
import ADS1256
import DAC8532

# smart plug libraries
from smartplug import SmartPlug
import Reco4lifeP10A as Reco

# database library
import pymysql

# GUI library
# import tkinter

# GPIO setting
GPIO.setmode(GPIO.BCM)

# device_setting
Humidifier_setting = ("192,168,1,100", "EdiMax")
Heater_setting = ("192.168.1.101", "EdiMax")
Fan0_setting = ("192.168.1.105", "Reco4life")
Fan1_setting = ("192.168.1.106", "Reco4life")
Pump_setting = ("192.168.1.103", "Reco4life")
Light_setting = ("","Reco4life")
DHT22_pin = 17

# value limits
light_limit_low = 25
# light_limit_high = 90
temperature_limit_low = 22
temperature_limit_high = 28
humidity_limit_low = 65
humidity_limit_high = 99
moisture_limit_low = 100
collection_frequency = 30*60

# program setting
print_val = True

# private class for smart plugs control (combine into one object)
class Device:
    def __init__(self, ip, type):
        self._IP = ip
        self._type = type
        self.setup()

    def setup(self):
        if self._type == "Edimax":
            self._device = SmartPlug(self._IP, ('admin', 'password'))

    def on(self):
        if self._type == "Edimax":
            self._device.state = 'ON'
        elif self._type == "Reco4life":
            Reco.on(self._IP)

    def off(self):
        if self._type == "Edimax":
            self._device.state = 'OFF'
        elif self._type == "Reco4life":
            Reco.off(self._IP)

# Device inits
Humidifier = Device(Humidifier_setting[0], Humidifier_setting[1])
Heater = Device(Heater_setting[0], Heater_setting[1])
Fan0 = Device(Fan0_setting[0], Fan0_setting[1])
Fan1 = Device(Fan1_setting[0], Fan1_setting[1])
Pump = Device(Pump_setting[0], Pump_setting[1])
Light = Device(Light_setting[0], Light_setting[1])


def main_loop():
    # init the device state
    light_state = False
    waterpump_state = False
    humidifier_state = False
    heater_state = False
    fan0_state = False
    fan1_state = False

    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()

    while True:
        # data collection
        # AD-DA module
        try:
            ADC_Value = ADC.ADS1256_GetAll()
            light_0 = ADC_Value[0]*5.0
            light_1 = ADC_Value[1]*5.0
            CO2_0 = ADC_Value[2]*5.0
            CO2_1 = ADC_Value[3]*5.0
            moisture_0 = ADC_Value[4]*5.0
            moisture_1 = ADC_Value[5]*5.0
            moisture_2 = ADC_Value[6]*5.0
            moisture_3 = ADC_Value[7]*5.0
        except :
            GPIO.cleanup()
            print ("AD module interrupted")
            # exit()

        # DHT22
        DHT22 = Adafruit_DHT.DHT22
        humidity22, temperature22 = Adafruit_DHT.read_retry(DHT22, DHT22_pin)
        try:
            humidity22 = int(humidity22)
            temperature22 = int(temperature22)
        except:
            print ("DHT22 read failure")
            humidity22 = 0
            temperature22 = 0

        if print_val:
            print ("light_0: %i, light_1: %i"%(ADC_Value[0]*5.0,ADC_Value[1]*5.0))
            print ("CO2_0: %i, CO2_1: %i"%(ADC_Value[2]*5.0,ADC_Value[3]*5.0))
            print ("moisture_0: %i, moisture_1: %i, moisture_2: %i, moisture_3: %i"%(ADC_Value[4]*5.0,ADC_Value[5]*5.0,ADC_Value[6]*5.0,ADC_Value[7]*5.0))
            if (humidity22 == 0 and temperature22 == 0):
                print("DHT22 failure")
            else:
                print("DHT22: humidity = %i, temperature = %i" % (humidity22, temperature22))

        # database storage
        conn=pymysql.connect(host='localhost',
                             port=3306,
                             user='Greenhouseadmin',
                             password='adminpassword',
                             db='GreenhouseDB',
                             charset='utf8')
        cur=conn.cursor()
        sql = """INSERT INTO test (time,sensor_light_0,sensor_light_1,sensor_CO2_0,sensor_CO2_1,sensor_moisture_0,sensor_moisture_1,sensor_moisture_2,sensor_moisture_3,sensor_temperature,sensor_humidity,device_light,device_waterpump,device_fan_0,device_fan_1,device_humidifier,device_heater) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        val = (datetime.datetime.now(), light_0, light_1, CO2_0, CO2_1, moisture_0, moisture_1, moisture_2, moisture_3, temperature22, humidity22, light_state, waterpump_state, fan0_state, fan1_state, humidifier_state, heater_state)
        cur.execute(sql,val)
        conn.commit()
        cur.close()
        conn.close()
        


        # Light
        if light_1 > light_limit_low and not light_state:
            Light.on()
            light_state = True
        elif light_1 <= light_limit_low and light_state:
            Light.off()
            light_state = False


        # Temperature
        if temperature22 < temperature_limit_low and temperature22 != 0:
            # if the temperature is low, turn on the heater and the fan to warm the greenhouse
            fan0_state = True
            fan1_state = True
            heater_state = True

            Fan0.on()
            Fan1.on()
            device_control(Heater,collection_frequency,15,105)

        elif temperature22 > temperature_limit_high and temperature22 != 0:
            # if the temperature is high, turn on the fan to circulate the air to cool the greenhouse down. at the same time, turn on the humidifier to accelerate the cooling 
            fan0_state = True
            fan1_state = True
            humidifier_state = True

            Fan0.on()
            Fan1.on()
            device_control(Humidifier,collection_frequency,30,30)

        else:
            Fan0.off()
            Fan1.on()
            fan0_state = False
            fan1_state = True
            humidifier_state = False
            heater_state = False

        # humidity
        if humidity22 < 65 and humidity22 != 0 and not humidifier_state:
            humidifier_state = True
            device_control(Humidifier,collection_frequency,15,105)

        # moisture
        if ((moisture_0 + moisture_1 + moisture_2 + moisture_3) / 4) > 150:
            Pump.on()
            waterpump_state = 'ON'
            time.sleep(10)
            Pump.off()

        if water_timer >= 23:
            Reco.on('192.168.1.103')
            waterpump_state = 'ON'
            time.sleep(30)
            Reco.off('192.168.1.103')
            water_timer = 0
        else:
            water_timer += 1



        # keep collecting the data base on the frequency setting
        time.sleep(collection_frequency)


# helper fun for device control
def device_control(device, duration, on_time, off_time):
    t = threading.Thread(target=device_control_helper(device,duration,on_time,off_time))
    t.start()


def device_control_helper(device, duration, on_time, off_time):
    for i in range(duration/ (on_time + off_time)):
        device.on()
        time.sleep(on_time)
        device.off()
        time.sleep(off_time)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        pass
