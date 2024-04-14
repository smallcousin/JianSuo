'''
Author: CHaNjIU 502744746@qq.com
Date: 2023-11-21 16:24:33
LastEditors: CHaNjIU 502744746@qq.com
LastEditTime: 2023-12-18 16:53:07
FilePath: \GEE\pygee.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# 检索图像的代码
import ee
import os
import glob
import datetime
import pandas as pd
import requests
#设置网络代理端口,7890为自己的端口号
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['ALL_PROXY']='http://127.0.0.1:7890'
# from SIAC import SIAC_S2

ee.Initialize()
# image1 = ee.Image('srtm90_v4')
# path = image1.getDownloadUrl({
#     'scale': 30,
#     'crs': 'EPSG:4326',
#     'region': '[[-120, 35], [-119, 35], [-119, 34], [-120, 34]]'
# })
# 获取下载地址
# print(path)

# 要查询的csv文件路径
# data_root = r".\csvFile"
# csv_paths = glob.glob(data_root+"\\*.csv")


# DOX2_ADJUSTED (micromole/kg)  CPHL_ADJUSTED (milligram/m3)  PHPH (none)

# 查询的参数
# param = "DOX2_ADJUSTED (micromole/kg)"


# 大气处理
def mask_s2_clouds(image):
  """Masks clouds in a Sentinel-2 image using the QA band.

  Args:
      image (ee.Image): A Sentinel-2 image.

  Returns:
      ee.Image: A cloud-masked Sentinel-2 image.
  """
  qa = image.select('QA60')

  # Bits 10 and 11 are clouds and cirrus, respectively.
  cloud_bit_mask = 1 << 10
  cirrus_bit_mask = 1 << 11

  # Both flags should be set to zero, indicating clear conditions.
  mask = (
      qa.bitwiseAnd(cloud_bit_mask)
      .eq(0)
      .And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
  )

  return image.updateMask(mask).divide(10000)


# 淑如开始时间与坐标信息，查询是否有图像
def processFeature(start_time , geom):
    # op: 0：L1C   1:landsat
    op = 0
    # 弄这么大范围的空间
    centerGeometry = geom.buffer(1000/2) \
                        .bounds() \
                        .buffer(1000/2)

    # 大气图像处理，排序，找出最清晰的那张（先找sentinel的）
    sentinel_collection  = ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
        .filterBounds(centerGeometry) \
        .filterDate(start_time.advance(-12,'hour'),start_time.advance(12,'hour')) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 2)) \
        .sort('CLOUDY_PIXEL_PERCENTAGE')   # 对应时间前后十二小时的图像
#         .map(maskS2clouds)
    # print(landsat_collection)
    Image = ee.Image(sentinel_collection .first())
    # print(sentinelImage.getInfo())
#     print(sentinelL2AImage.getInfo())
#     info = sentinelL2AImage.getInfo()
    # landsat图像获取，不做这个
    # if Image.getInfo() is None :
    #     landsat_collection  = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
    #         .filterBounds(centerGeometry) \
    #         .filterDate(start_time,start_time.advance(1,'day')) \
    #         .filter(ee.Filter.lt('CLOUDY_COVER', 2)) \
    #         .sort('CLOUDY_COVER')
    #     Image = ee.Image(landsat_collection .first())
    #     if Image.getInfo() == None:
    #         return None , 0
    #     else:
    #         op = 1
        # if Image.getInfo() == None:
        #     landsat_collection  = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
        #     .filterBounds(centerGeometry) \
        #     .filterDate(start_time,start_time.advance(1,'day')) \
        #     .filter(ee.Filter.lt('CLOUDY_COVER', 2)) \
        #     .sort('CLOUDY_COVER')
        #     Image = ee.Image(landsat_collection .first())
        #     if Image.getInfo()==None:
        #         return None
        #     else:
        #         op=2
        # else:
        #     op = 1 
    # landsatImage = landsatImage.select(['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12'])
    if Image.getInfo() is None:
        return None
    return Image

def search():
    # 读取文件夹里的所有文件
    # pathName = "./excel2"
    # file_names = os.listdir(pathName)
    print("开始读取文件")
    df = pd.read_excel("./excel/胥湖心水质数据.xlsx", usecols=["发布时间"]).drop_duplicates()
    date_list = df["发布时间"]
    print("读取文件成功")
    print("date_list的类型：",type(date_list))
    # print("CPHL_ADJUSTED (milligram/m3)" in columns)
    # Latitude,Longitude,Time
    lon = 120.4318
    lat = 31.1593
    centerGeometry = ee.Geometry.Point([lon, lat])
    for search_date in date_list:
        print("进入循环")
        # print(lon , lat , search_date)
        # 测试用
        # lat , lon = 23.13,113.26
        # search_date = "2023-03-05T12:14:55Z"
        # print(lon,lat , type(lon) , type(lat))
        # 设置日期格式
        # 第一行不是时间，是列名，所以要跳过一下
        print("search_date的类型：", type(search_date))
        try:
            # 转化时间为国际时间
            dateT = datetime.datetime.strptime(search_date,'%Y-%m-%d %H:%M:%S').isoformat()
            print(dateT)
        except ValueError:
            print("Skipping line: not a valid date -", search_date)
            continue
        # date = date.strftime('%Y-%m-%d')
        # print(dateT)
        # 转为gee的日期
        date = ee.Date(dateT)

        # print(date)
        # 检索这个日期的图像
        product = processFeature(date , centerGeometry)


        print(f'date:{dateT} , lon:{lon} , lat:{lat} , product:{product.get("id").getInfo() if product is not None  else None}')
        if product is not None:

            id = product.get('PRODUCT_ID').getInfo()

            text = dateT + "," + str(lon) + "," + str(lat) + ","  +  id + "\n"
            with open('./csvFile/胥湖心水质数据检索得到的图像.csv','a', encoding = 'utf-8') as f:
                    f.write(text)
                    f.close()

# 主函数  开始函数
if __name__ == '__main__':
    search()
# date = ee.Date('2021-05-01')
# centerGeometry = ee.Geometry.Point(-114.2579, 38.9275)
# print(processFeature(date , centerGeometry))