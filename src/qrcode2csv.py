import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import os

# 读取图片
image_path = './image.jpg'
image = cv2.imread(image_path)
absolute_path = os.path.abspath(image_path)
print("读取的二维码图片路径:", absolute_path) 

# 将图片转为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用pyzbar库解码二维码
barcodes = decode(gray)

# 遍历解码结果
for barcode in barcodes:
    # 提取二维码的数据
    rawData = barcode.data.decode('utf-8')

print(f"二维码原始数据: {rawData}")

code_name = rawData[0:13]
print(f'光谱编号：{code_name}')
lightData = rawData[13:]
# 初始化一个空数组
result_array = []

# 将每一组16位提取出来，放到数组中
for i in range(0, len(lightData), 16):
    group = lightData[i:i+16]
    result_array.append(group)

# 创建一个 pandas 数据框
df = pd.DataFrame({code_name: result_array})
print('16进制光谱数据:')
print(df)

# 定义一个函数，用于将16位数拆分成两位一组，并转换为10进制
def split_16_bits_and_convert(value):
    return [int(value[i:i+2], 16) for i in range(0, len(value), 2)]

# 在数据框中应用这个函数，得到一个包含8列的数据框
new_columns = pd.DataFrame(df[code_name].apply(split_16_bits_and_convert).tolist(), columns=[f'col{i+1}' for i in range(8)])

# 将新列连接到原始数据框
df = pd.concat([df, new_columns], axis=1)

new_column_names = {'col1': '时', 'col2': '分', 'col3': '白', 'col4': '蓝',
                    'col5': '绿', 'col6': '紫', 'col7': '浅蓝', 'col8': '红'}

# 使用 rename 方法重命名列
df = df.rename(columns=new_column_names)

# 显示更新后的数据框
print('处理后的光谱数据:')
print(df)

# df保存为csv，ansi编码，便于excel打开显示中文字符
csv_file_path = './spectrum.csv'
absolute_path = os.path.abspath(csv_file_path)
df.to_csv(csv_file_path, index=False, encoding='ansi')
print("光谱表格保存路径:", absolute_path)


