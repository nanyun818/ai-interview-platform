import os
import datetime

# 检查文件的修改时间
file_path = 'e:/ai-interview-platform/app.py'
if os.path.exists(file_path):
    modified_time = os.path.getmtime(file_path)
    print(f"文件最后修改时间: {datetime.datetime.fromtimestamp(modified_time)}")
else:
    print("文件不存在")