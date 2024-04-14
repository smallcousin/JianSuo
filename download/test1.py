import ee
ee.Initialize()
image1 = ee.Image('srtm90_v4')
path = image1.getDownloadUrl({
   'scale': 30,
   'crs': 'EPSG:4326',
   'region': '[[-120, 35], [-119, 35], [-119, 34], [-120, 34]]'
})
# 获取下载地址
print(path)