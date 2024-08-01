import os
from datetime import datetime

def copy_and_overwrite_files_in_subfolders(base_folder_path):
    # 遍历当前文件夹下的所有子文件夹
    for root, dirs, files in os.walk(base_folder_path):
        for file in files:
            if file.endswith((".xlsx", ".xls", ".pdf", ".docx")):
                file_path = os.path.join(root, file)

                try:
                    # 读取文件内容
                    with open(file_path, 'rb') as f:
                        file_content = f.read()

                    # 写回文件以覆盖原文件
                    with open(file_path, 'wb') as f:
                        f.write(file_content)
                                                 
                    # 更新文件的修改时间
                    current_time = datetime.now().timestamp()
                    os.utime(file_path, (current_time, current_time))
                    print(f"已覆盖并更新元数据的文件: {file_path}")

                except Exception as e:
                    print(f"处理文件 {file} 时发生错误: {e}")

# 示例用法
base_folder_path = "."
copy_and_overwrite_files_in_subfolders(base_folder_path)
