import os
import time

# 等待一段时间，确保报告有足够时间生成
print('等待5秒...')
time.sleep(5)

# 使用原始字符串避免转义序列问题
report_path = r'E:\ai-interview-platform\interview_report.pdf'
print(f'检查报告文件是否存在: {report_path}')
if os.path.exists(report_path):
    print(f'报告文件存在，大小: {os.path.getsize(report_path)} 字节')
    # 尝试打开文件查看内容
    try:
        with open(report_path, 'rb') as f:
            content = f.read(100)
            print(f'报告文件前100个字节: {content}')
    except Exception as e:
        print(f'无法读取文件内容: {str(e)}')
else:
    print('报告文件不存在')
    # 列出目录内容，看看有什么文件
    dir_path = r'E:\ai-interview-platform'
    print(f'列出目录 {dir_path} 中的文件:')
    try:
        files = os.listdir(dir_path)
        for file in files:
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                print(f'文件: {file}, 大小: {os.path.getsize(file_path)} 字节')
    except Exception as e:
        print(f'无法列出目录内容: {str(e)}')