import os
import shutil

def copy_and_rename_excel_files(folder_path):
    # 遍历文件夹中的所有Excel文件
    for file in os.listdir(folder_path):
        if file.endswith(".xlsx") or file.endswith(".xls"):
            file_path = os.path.join(folder_path, file)
            new_file_name = "新的_" + file
            new_file_path = os.path.join(folder_path, new_file_name)
            
            # 复制文件并重命名
            try:
                shutil.copy(file_path, new_file_path)
                print(f"已创建文件: {new_file_name}")
            except Exception as e:
                print(f"复制文件 {file} 时发生错误: {e}")

# 示例用法
folder_path = './2023'
copy_and_rename_excel_files(folder_path)
