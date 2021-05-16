import pandas as pd
import pymysql
import datetime
import threading

# ## 加上字符集参数，防止中文乱码
# dbconn=pymysql.connect(
#   host="localhost",
#   database="GreenhouseDB",
#   user="Greenhouseadmin",
#   password="adminpassword",
#   port=3306,
#   charset='utf8'
#  )

# #sql语句
# # sqlcmd="select time,light_level from test_table limit 256"
# # sqlcmd="select time,sensor_light_0,sensor_light_1,sensor_CO2_0,sensor_CO2_1,sensor_moisture_0,sensor_moisture_1,sensor_moisture_2,sensor_moisture_3,sensor_temperature,sensor_humidity,device_light,device_waterpump,device_fan_0,device_fan_1,device_humidifier,device_heater from test limit 256"
# sqlcmd = "select * from test order by id desc limit 1"
# #利用pandas 模块导入mysql数据
# df=pd.read_sql(sqlcmd,dbconn)
# #取前5行数据
# print(df.to_dict('list'))

# def user_control_tag(device_name):
#   t = threading.Thread(target=store,args=[device_name])
#   t.start()

# def store(device_name):
#   conn=pymysql.connect(host='localhost',
#                             port=3306,
#                             user='Greenhouseadmin',
#                             password='adminpassword',
#                             db='GreenhouseDB',
#                             charset='utf8')
#   cur=conn.cursor()
#   sql = "INSERT INTO user_control (time, " + device_name + ") VALUES (%s, %s);"
#   val = ( datetime.datetime.now(), True)
#   cur.execute(sql,val)
#   conn.commit()
#   cur.close()
#   conn.close()


# user_control_tag("light")