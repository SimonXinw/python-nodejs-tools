import pandas as pd
import json
import os
import copy

# 新文件的名字
new_excel_name = 'new.xlsx'

# 获取当前工作目录
current_dir = os.getcwd()

# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(__file__)

# 1 - 要取的 excel 文件的在当前文件夹的相对路径，这里有两个，如果要新增变量和文件的话，注意变量名和数量也要对应的增加
raw_excel_1_relative_path = "raw_excel/原数据.xlsx"

# 2 - 第二个
raw_excel_2_relative_path = "raw_excel/新数据差异.xlsx"

# 1 - 产出的第一个文件的相对路径，对应的当前文件夹的当前路径
new_excel_relative_path = f"new_excel/{new_excel_name}"

raw_excel_1_file_path = os.path.join(current_dir, raw_excel_1_relative_path)

raw_excel_2_file_path = os.path.join(current_dir, raw_excel_2_relative_path)

new_excel_file_path = os.path.join(current_dir, new_excel_relative_path)

print("新工作目录:", new_excel_file_path)


# 读取 Excel 文件
excel_file_1 = pd.read_excel(raw_excel_1_file_path)

excel_file_2 = pd.read_excel(raw_excel_2_relative_path)

# 将数据转换为 JSON
json_data_1 = excel_file_1.to_json(orient='records')

json_data_2 = excel_file_2.to_json(orient='records')

#  定义处理 json 数据逻辑


def add_numbers(_json_1, _json_2):
    _list_1 = json.loads(_json_1)
    _list_2 = json.loads(_json_2)

    new_list_2 = copy.deepcopy(_list_2)

#  处理逻辑
    for hero_2 in new_list_2:

        for hero_1 in _list_1:
            if hero_2['英雄'] == hero_1['英雄']:
                if hero_2['星级'] == hero_1['星级']:
                    hero_2['差异'] = 1
                    break

# 将 null 或者空格 转换成 1
    for hero_2 in new_list_2:
        if hero_2['差异'] != 1:
            hero_2['差异'] = 0

    print('json >>>>>>', new_list_2)
    return new_list_2


# 执行
result_excel = add_numbers(json_data_1, json_data_2)

json_result_excel = json.dumps(result_excel)

# 将 JSON 转换为 DataFrame
new_excel = pd.read_json(json_result_excel)

# 将 DataFrame 写入 Excel 文件
new_excel.to_excel(new_excel_file_path, index=False)
