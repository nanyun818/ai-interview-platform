import PyPDF2
import os

# 检查文件是否存在
pdf_path = 'interview_report.pdf'
if os.path.exists(pdf_path):
    print(f'文件存在: {pdf_path}')
    # 打开PDF文件
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        # 提取第一页文本
        page = reader.pages[0]
        text = page.extract_text()
        print('PDF内容:')
        print(text)
else:
    print(f'文件不存在: {pdf_path}')