import pandas as pd
import json


# 将json格式文件转化为excel文件，同时修改一下列名

def changeJsonfileToExcel():
    json_file = "./jsonFile/广东省流域数据.json"
    output_excel_file = "./excel/广东省流域数据.xlsx"
    with open(json_file, 'r', encoding='utf-8') as file:
        df = pd.read_json(file)
    data_df = pd.DataFrame(df['data'].tolist())
    # 改变列名
    new_column_names = {
        'province': '广东省',
        'city': '城市',
        'valley': '流域',
        'staname': '站点名称',
        'longitude': '经度',
        'latitude': '维度',
        'first_time': '数据开始统计时间',
        'last_time': '最后统计时间'
    }
    data_df = data_df.rename(columns=new_column_names)
    print('开始转化')
    data_df.to_excel(output_excel_file, index=False, engine='openpyxl')

    print('转换成功')


if __name__ == '__main__':
    changeJsonfileToExcel()
    print('成功结束')
