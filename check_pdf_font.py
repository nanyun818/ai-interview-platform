import PyPDF2
import sys

def check_pdf_font(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            # 获取PDF的元数据
            metadata = reader.metadata
            print(f"PDF元数据: {metadata}")

            # 检查第一页的内容
            if len(reader.pages) > 0:
                page = reader.pages[0]
                text = page.extract_text()
                print(f"PDF文本内容 (前100个字符): {text[:100]}")

            # 检查字体
            print("检查PDF中的字体...")
            # 注意: PyPDF2不能直接获取字体信息，这里只是尝试提取文本

    except Exception as e:
        print(f"处理PDF时出错: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = 'downloaded_report.pdf'
    check_pdf_font(pdf_path)