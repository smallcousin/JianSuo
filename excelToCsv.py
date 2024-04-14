import pandas as pd

# Read Excel file
excel_file = r'.\excel\监测站水质数据.xlsx'
df = pd.read_excel(excel_file)

# 筛选出第一列（假设名为'Location'）为“新丰江水库”的行
filtered_df = df[df['水库名'] == '新丰江水库']

# 将固定经纬度23.845518,114.554647和第二列的值写入新的DataFrame
new_df = pd.DataFrame({
  'Latitude': 23.845518,
  'Longitude': 114.554647,
  'Time': filtered_df['时间']
})

# 将新的DataFrame写入CSV文件，假设文件名为'output.csv'
csv_file_path = 'csvFile/output.csv'
new_df.to_csv(csv_file_path, index=False)

# 显示操作成功的消息
print("成功将excel文件的相关信息写入csv文件")