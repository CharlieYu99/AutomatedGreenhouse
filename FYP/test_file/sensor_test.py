import Adafruit_DHT
import time

import ADS1256
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
ADC = ADS1256.ADS1256()
ADC.ADS1256_init()


# # DHT22_pin = 4
DHT22_pin_in = 18
DHT22_pin_out = 4

# #  DHT22
# DHT22 = Adafruit_DHT.DHT22
# try:
#     humidity22, temperature22 = Adafruit_DHT.read_retry(DHT22, DHT22_pin)
# except:
#     print ("DHT22 failure")

# try:
#     humidity22 = int(humidity22)
#     temperature22 = int(temperature22)
# except:
#     print ("DHT22 read failure")
#     humidity22 = 0
#     temperature22 = 0

# if (humidity22 == 0 and temperature22 == 0):
#     print("DHT22 failure")
# else:
#     print("DHT22: humidity = %i, temperature = %i" % (humidity22, temperature22))


# import Adafruit_DHT

# # Sensor should be set to Adafruit_DHT.DHT11,
# # Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
# sensor = Adafruit_DHT.DHT22

# # Example using a Beaglebone Black with DHT sensor
# # connected to pin P8_11.
# # pin = 'P8_11'

# # Example using a Raspberry Pi with DHT sensor
# # connected to GPIO23.
# pin = 18

# # Try to grab a sensor reading.  Use the read_retry method which will retry up
# # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
# humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# # Note that sometimes you won't get a reading and
# # the results will be null (because Linux can't
# # guarantee the timing of calls to read the sensor).
# # If this happens try again!
# if humidity is not None and temperature is not None:
#     print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
# else:
#     print('Failed to get reading. Try again!')


DHT22_pin_in = 18
DHT22_pin_out = 4

DHT22 = Adafruit_DHT.DHT22
# DHT22_in = Adafruit_DHT.DHT22
# DHT22_out = Adafruit_DHT.DHT22

while True:
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

    if True:
        if (humidity22_in == 0 and temperature22_in == 0):
            print("DHT22 inside failure")
        else:
            print("DHT22 inside: humidity = %i, temperature = %i" % (humidity22_in, temperature22_in))
        if (humidity22_out == 0 and temperature22_out == 0):
            print("DHT22 outside failure")
        else:
            print("DHT22 ouside: humidity = %i, temperature = %i" % (humidity22_out, temperature22_out))
    time.sleep(10)





# while True:
#     try:
#         ADC_Value = ADC.ADS1256_GetAll()
#         light_0 = int(ADC_Value[0])
#         light_1 = int(ADC_Value[1])
#         CO2_0 = int(ADC_Value[2])
#         CO2_1 = int(ADC_Value[3])
#         moisture_0 = int(ADC_Value[4])
#         moisture_1 = int(ADC_Value[5])
#         moisture_2 = int(ADC_Value[6])
#         moisture_3 = int(ADC_Value[7])

#         print ("light_0: %i, light_1: %i"%(ADC_Value[0],ADC_Value[1]))
#         print ("CO2_0: %i, CO2_1: %i"%(ADC_Value[2],ADC_Value[3]))
#         print ("moisture_0: %i, moisture_1: %i, moisture_2: %i, moisture_3: %i"%(ADC_Value[4],ADC_Value[5],ADC_Value[6],ADC_Value[7]))
        
#     except :
#         GPIO.cleanup()
#         print ("AD module interrupted")
#         # exit()
#     time.sleep(3)