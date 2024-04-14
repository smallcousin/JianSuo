import csv
from datetime import datetime

def convert_to_utc(time_str):
  """将时间字符串从YYYYMMDDTHHMMSS格式转换为UTC格式"""
  dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
  return dt.isoformat()

def process_line(line):
  """处理每一行，截取第二列到第四列，并转换时间"""
  parts = line.split()
  if len(parts) < 4:
    return None  # 行中不足4列数据
  adjusted_line = parts[4:5] + parts[3:4]
  time_line = convert_to_utc(" ".join(parts[1:3]))  # 转换时间
  return adjusted_line + [time_line]  # 返回第二列到第四列

def convert_file(input_file, output_file):
  """转换文件内容"""
  with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    headers = ['Latitude', 'Longitude', 'Time']
    writer.writerow(headers)
    for line in infile:
      processed_line = process_line(line)
      if processed_line:
        writer.writerow(processed_line)

# 使用函数转换文件
if __name__ == '__main__':
  print("开始处理文件")
  convert_file('./新丰江水质数据检索得到的图像.csv', './csvFile/处理结果.csv')
  print("处理完成")