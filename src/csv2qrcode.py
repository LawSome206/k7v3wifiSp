import pandas as pd
import os
import qrcode

# 读取 CSV 文件
csv_file_path = "./spectrum.csv"  # 替换为你的 CSV 文件路径
absolute_path = os.path.abspath(csv_file_path)
df = pd.read_csv(csv_file_path, encoding='ansi')
print("读取的光谱表格路径:", absolute_path)

# 显示 DataFrame 的前几行
print("光谱数据:")
print(df)

code_name = df.columns[0]  # 记录光谱二维码开头数据

df1 = df.iloc[:, -8:]

# 将每一列的十进制数字转换为十六进制并进行零填充
df_hex = df1.apply(lambda x: x.apply(lambda y: format(y, 'x').zfill(2)))

# 将八列的十六进制数字拼接在一起
df_concatenated = df_hex.apply(lambda x: ''.join(x), axis=1)

column_as_strings = df_concatenated.astype(str)

# 使用字符串连接操作拼接所有字符串
result_string = ''.join(column_as_strings)
result_string = code_name + result_string
# 打印结果
print('即将生成二维码的原始数据:',result_string)

# 创建QRCode对象
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# 添加数据到QRCode对象
qr.add_data(result_string)
qr.make(fit=True)

# 创建PIL图像对象
img = qr.make_image(fill_color="black", back_color="white")

qrcode_file_path = "./qrcode.jpg"
absolute_path = os.path.abspath(qrcode_file_path)
# 保存图像文件
img.save(qrcode_file_path)

print("二维码已生成并保存到:")
print(absolute_path)
