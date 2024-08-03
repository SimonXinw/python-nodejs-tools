import pandas as pd
import re
from time import time

# 文件路径
file1_path = 'C:\\Users\\simon\\Desktop\\python-projects\\python-tools\\高考全国院校投档线-文件转换_数据清洗\\江西\\2024\\院校招生专业组专业明细.xlsx'
file2_path = 'C:\\Users\\simon\\Desktop\\python-projects\\python-tools\\高考全国院校投档线-文件转换_数据清洗\\江西\\2024\\江西省2024年普通高校招生本科投档情况统计表(历史类、物理类、三校生类).xlsx'

# 计时开始
start_time = time()

# 读取文件
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

# 清洗数据，确保列名和数据一致
df1 = df1[['院校名称', '专业组', '选科', '包含专业']]
df2 = df2.rename(columns={'专业组名称': '专业组', '专业': '包含专业'})

# 清洗df2中的专业组，移除“第”和“组”以及括号中的内容
df2['专业组'] = df2['专业组'].apply(lambda x: re.sub(r'第|组|\(.*?\)', '', x).strip())

# 创建唯一键
df1['key'] = df1['院校名称'] + '-' + df1['专业组'].astype(str)
df2['key'] = df2['院校名称'] + '-' + df2['专业组'].astype(str)

# 合并数据
df2 = df2.merge(df1[['key', '选科', '包含专业']], on='key', how='left', suffixes=('', '_new'))

# 用表1的值填充表2的对应列
df2['选科'] = df2['选科_new'].combine_first(df2['选科'])
df2['包含专业'] = df2['包含专业_new'].combine_first(df2['包含专业'])

# 删除临时列
df2.drop(columns=['选科_new', '包含专业_new', 'key'], inplace=True)

# 保存更新后的文件
df2.to_excel(file2_path, index=False)

# 计时结束
end_time = time()
print(f"处理时间: {end_time - start_time:.2f} 秒")
    