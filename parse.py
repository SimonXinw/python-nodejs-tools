import os
import shutil

def copy_and_overwrite_files_in_subfolders(base_folder_path):
    # 遍历当前文件夹下的所有子文件夹
    for root, dirs, files in os.walk(base_folder_path):
        for file in files:
            if file.endswith((".xlsx", ".xls", ".pdf")):
                file_path = os.path.join(root, file)
                temp_file_path = os.path.join(root, "temp_" + file)
                
                # 复制文件到临时文件
                try:
                    shutil.copy(file_path, temp_file_path)
                    print(f"已创建临时文件: {temp_file_path}")
                    
                    # 覆盖原文件
                    shutil.move(temp_file_path, file_path)
                    print(f"已覆盖原文件: {file_path}")
                except Exception as e:
                    print(f"复制文件 {file} 时发生错误: {e}")

# 示例用法
base_folder_path = '.'
copy_and_overwrite_files_in_subfolders(base_folder_path)
