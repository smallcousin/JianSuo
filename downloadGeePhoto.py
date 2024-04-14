import ee
from ee import batch
from ee.batch import Export
from ee.ee_exception import EEException
import time
from SIAC import SIAC_S2

# 初始化 Earth Engine API
ee.Initialize()
#
# 加载CSV文件
csv_asset = 'projects/ee-chenhongchao79/assets/newOutput'  # 替换成你的用户名和CSV文件路径
csv_table = ee.FeatureCollection(csv_asset)

# 输出文件夹
output_folder = 'sentinel1'  # 替换为你希望保存TIFF文件的文件夹名称


# 云掩膜函数
def mask_s2_clouds(image):
    qa = image.select('QA60')
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11
    mask = qa.bitwiseAnd(cloud_bit_mask).eq(0) \
        .And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
    return image.updateMask(mask)


# 处理每个要素的函数
def process_feature(feature):
    lat = float(ee.Number(feature.get('lat')).format('%.5f'))
    lon = float(ee.Number(feature.get('lon')).format('%.5f'))
    start_time = ee.Date(feature.get('start_time'))
    center_geometry = ee.Geometry.Point(lon, lat).buffer(700 / 2) \
        .bounds() \
        .buffer(700 / 2)

    s1c = ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
        .filterBounds(center_geometry) \
        .filterDate(start_time, start_time.advance(1, 'day')) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 2)) \
        .sort('CLOUDY_PIXEL_PERCENTAGE')

    s2_boa = s1c.first()

    # image_region = center_geometry.buffer(300 / 2) \
    #     .bounds() \
    #     .buffer(300 / 2)
    #
    # s2_boa = s2_boa.set('lon', lon).set('lat', lat).clip(image_region)

    return s2_boa


# 处理所有要素
processed_images = csv_table.map(process_feature)

# 过滤结果
processed_images = processed_images.filter(ee.Filter.listContains('system:band_names', 'B2'))


# 导出图像集合到Drive
def export_image_collection(img_col, output_folder):
    try:
        # 获取索引列表
        index_list = img_col.reduceColumns(ee.Reducer.toList(), ["system:index"]).get("list")
        index_list.evaluate(lambda indexs:
                            [Export.image.toDrive({
                                'image': img_col.filter(ee.Filter.eq("system:index", index)).first(),
                                'description': f'csv0_{index}',
                                'folder': output_folder,
                                'scale': 10,
                                'maxPixels': 1e13,
                                'fileFormat': 'GeoTIFF'
                            }) for index in indexs])
    except EEException as e:
        print(f'An error occurred: {e}')


export_image_collection(processed_images, output_folder)

# 等待任务完成
while batch.active():
    print("Waiting for tasks to complete...")
    time.sleep(60)  # 每分钟检查一次
