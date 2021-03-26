import datetime
from sunrise_sunset import SunriseSunset

# geography position (Suzhou for the below setting)
longitude = 120.62
latitude = 31.32
timezone_offset = 8


time_now = datetime.datetime.now().strftime("%H:%M:%S")
print(time_now)

ro = SunriseSunset(datetime.datetime.now(), latitude=latitude, longitude=longitude, localOffset=timezone_offset)
rise_time, set_time = ro.calculate()
rise_time = rise_time.strftime("%H:%M:%S")
print(rise_time)

print(time_now > rise_time)

