import pandas as pd
import os

'''
把获取到的遥感图像按照日期进行重命名
'''

# 设置CSV文件路径和图片目录
csv_path = './csvFile/'  # 日期的路径
image_dir = './newPhoto/'  # 遥感图像的路径
# output_dir = ''

# output_dir = image_dir + "/万子湖"
place = [
    "万子湖",
    "东半湖湖心",
    "东洞庭湖",
    "新丰江水库",
    "滇池南",
    "石骨水库",
    "胥湖心",
    "良德水库"
]
# placee = [
#     ["万子湖", 4],
#     ["东半湖湖心", 6],
#     ["东洞庭湖", 5],
#     ["新丰江水库", 6],
#     ["滇池南", 4],
#     ["石骨水库", 5],
#     ["胥湖心", 4],
#     ["良德水库", 5]
# ]
endText = "水质数据检索得到的图像"
# 读取CSV文件


for i in range(0, len(place)):
    # 读取csv文件，因为csv文件有endText的后缀，所以要加上
    data = pd.read_csv(csv_path + place[i] + endText + ".csv")
    print(f"len({place[i]})", len(place[i]))
    # 确保目录存在
    if not os.path.exists(image_dir + place[i]):
        os.makedirs(image_dir + place[i])

    # 获取目录中所有文件，比如新丰江目录下的所有文件
    files = os.listdir(image_dir + place[i])

    print("data", len(data))
    print("files", len(files))
    # 检查文件数量是否与日期匹配
    if len(files) != len(data):
        raise ValueError("图片数量和日期数量不匹配！")

    # 按照CSV文件中的日期重命名图片
    for index, file_name in enumerate(files):
        print(file_name)
        # 获取文件扩展名
        ext = os.path.splitext(file_name)[1]
        # 获取文件旧名
        file_old_name = os.path.splitext(file_name)[0]
        # 新文件名为日期加原始扩展名
        addressNameLength = len(place[i])  # 地址的长度，用来图片名字的长度，比如万子湖，需要截取“WZH_”
        new_name = file_old_name[:addressNameLength+1] + data.iloc[index, 0][:10] + "_" + file_old_name[-2:] + ext
        # 源文件和目标文件的完整路径
        src = os.path.join(image_dir + place[i], file_name)
        dst = os.path.join(image_dir + place[i], new_name)
        print("src:" + src)
        print("dst:" + dst)
        # 重命名操作
        os.rename(src, dst)

    print(f"{place[i]}的图片重命名完成。")