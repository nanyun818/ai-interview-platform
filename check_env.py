import sys
import os

# 打印Python解释器路径
print(f'Python解释器路径: {sys.executable}')

# 打印Python路径
print('\nPython路径:')
for path in sys.path:
    print(path)

# 检查PyPDF2是否存在于任何路径中
print('\n检查PyPDF2是否存在:')
found = False
for path in sys.path:
    if os.path.exists(os.path.join(path, 'PyPDF2')):
        print(f'在路径 {path} 中找到PyPDF2')
        found = True
        break
if not found:
    print('未找到PyPDF2')