from datetime import datetime
# Longitude,Latitude
import pandas
# 23.730313, 114.640567
fileName = 'csvFile/新丰江水库水质数据检索得到的图像.csv'

df = pandas.read_csv(fileName)
# 把日期转为国际日期
# df['Time'] = pandas.to_datetime(df['Time'])
# print(df['Time'])
# df['Time'] = df['Time'].dt.tz_localize('Asia/Shanghai').dt.tz_convert('UTC')
# df['Time'] = df['Time'].dt.strftime('%Y-%m-%dT%H:%M:%S')
# print(df['Time'])
# df.to_csv('./csvFile/XFJ.csv', index=False)
df['Longitude'] = 11
