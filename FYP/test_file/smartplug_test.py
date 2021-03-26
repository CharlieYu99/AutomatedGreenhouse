# smart plug libraries
from smartplug import SmartPlug
import Reco4lifeP10A as Reco

import time

# device_setting
Humidifier_setting = ("192.168.0.101", "Edimax")
Heater_setting = ("192.168.0.102", "Edimax")
Fan0_setting = ("192.168.0.104", "Reco4life")
Fan1_setting = ("192.168.0.115", "Reco4life")
Pump_setting = ("192.168.0.105", "Reco4life")
Light0_setting = ("192.168.0.103", "Reco4life")
Light1_setting = ("192.168.0.100","Reco4life")

#private class for smart plugs control (combine into one object)
class Device:
    def __init__(self, ip, _type):
        self._IP = ip
        self._type = _type
        # self._device = SmartPlug(self._IP, ('admin', 'password')) if self._type == "Edimax" else None 

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

# Device inits
Humidifier = Device(Humidifier_setting[0], Humidifier_setting[1])
Heater = Device(Heater_setting[0], Heater_setting[1])
# Fan0 = Device(Fan0_setting[0], Fan0_setting[1])
# Fan1 = Device(Fan1_setting[0], Fan1_setting[1])
# Pump = Device(Pump_setting[0], Pump_setting[1])
# Light0 = Device(Light0_setting[0], Light0_setting[1])
# Light1 = Device(Light1_setting[0], Light1_setting[1])

on_time = 5

Humidifier.on()
Heater.on()
time.sleep(on_time)
Heater.off()
Humidifier.off()
time.sleep(3)

# Fan0.on()
# time.sleep(on_time)
# Fan0.off()
# time.sleep(3)

# Fan1.on()
# time.sleep(on_time)
# Fan1.off()
# time.sleep(3)

# Pump.on()
# time.sleep(on_time)
# Pump.off()
# time.sleep(3)

# Light0.on()
# time.sleep(on_time)
# Light0.off()
# time.sleep(3)

# Light1.on()
# time.sleep(on_time)
# Light1.off()
# time.sleep(3)



# p1 = SmartPlug('192.168.0.102', ('admin', 'password'))
# p2 = SmartPlug('192.168.0.104', ('admin', 'password'))

# time.sleep(3)
# p1.state = 'ON'
# p2.state = 'ON'
# time.sleep(3)
# p1.state = 'OFF'
# p2.state = 'OFF'

# SmartPlug('192.168.0.102', ('admin', 'password')).state = 'ON'
# time.sleep(on_time)
# SmartPlug('192.168.0.102', ('admin', 'password')).state = 'OFF'