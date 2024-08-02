import pandas as pd
import time

# 文件路径
# file1_path = r'C:\Users\simon\Desktop\python-projects\python-tools\高考全国院校投档线-文件转换_数据清洗\江西\2024\院校招生专业组专业明细.xlsx'
# file2_path = r'C:\Users\simon\Desktop\python-projects\python-tools\高考全国院校投档线-文件转换_数据清洗\江西\2024\江西省2024年普通高校招生本科投档情况统计表(历史类、物理类、三校生类).xlsx'

file1_path = r'D:\projects\xw\python\python-tools\高考全国院校投档线-文件转换_数据清洗\江西\2024\院校招生专业组专业明细.xlsx'
file2_path = r'D:\projects\xw\python\python-tools\高考全国院校投档线-文件转换_数据清洗\江西\2024\江西省2024年普通高校招生本科投档情况统计表(历史类、物理类、三校生类).xlsx'


# 读取表1和表2
start_time = time.time()

df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

# 处理数据匹配并更新表2
for index1, row1 in df1.iterrows():
    majorCode =  str(row1['专业组']).split('（')[1].split('）')[0] 

    for index2, row2 in df2.iterrows():

        major2Code = row2['专业组名称']

        is_same_major_code = majorCode in major2Code

        if row1['院校名称'] == row2['院校名称'] and is_same_major_code :
            df2.at[index2, '专业'] = row1['包含专业']

# 计算处理时间
end_time = time.time()
processing_time = end_time - start_time
print(f"处理完成，总共用时 {processing_time:.2f} 秒。")

# 生成更新后的文件
file2_name = file2_path.split('\\')[-1]  # 获取原文件名
updated_file_path = file2_path.replace(file2_name, f"{file2_name}")

df2.to_excel(updated_file_path, index=False)
print(f"更新后的文件已保存为: {updated_file_path}")
