from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import sys

# 测试函数：尝试不同的方法来显示中文
def test_chinese_fonts():
    # 创建测试PDF文件
    pdf_path = 'test_chinese_font.pdf'
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    y_position = height - 50

    # 测试1: 使用默认字体
    c.setFont('Helvetica-Bold', 16)
    c.drawString(50, y_position, '1. 使用默认字体 (Helvetica):')
    y_position -= 20
    c.setFont('Helvetica', 12)
    c.drawString(70, y_position, '测试中文显示')
    y_position -= 40

    # 测试2: 尝试使用中文字体名称
    c.setFont('Helvetica-Bold', 16)
    c.drawString(50, y_position, '2. 尝试使用中文字体名称:')
    y_position -= 20
    try:
        c.setFont('SimHei', 12)
        c.drawString(70, y_position, '使用 SimHei 字体')
    except Exception as e:
        c.setFont('Helvetica', 12)
        c.drawString(70, y_position, f'错误: {str(e)}')
    y_position -= 20

    try:
        c.setFont('Microsoft YaHei', 12)
        c.drawString(70, y_position, '使用 Microsoft YaHei 字体')
    except Exception as e:
        c.setFont('Helvetica', 12)
        c.drawString(70, y_position, f'错误: {str(e)}')
    y_position -= 40

    # 测试3: 尝试注册系统字体
    c.setFont('Helvetica-Bold', 16)
    c.drawString(50, y_position, '3. 尝试注册系统字体:')
    y_position -= 20

    # 尝试注册常见的中文字体
    fonts_to_test = [
        ('SimHei', 'simhei.ttf'),
        ('Microsoft YaHei', 'msyh.ttf'),
        ('Arial Unicode MS', 'arialuni.ttf')
    ]

    for font_name, font_file in fonts_to_test:
        try:
            # 尝试在系统中查找字体文件
            # 注意：这只是一个简化的示例，实际上可能需要搜索更多路径
            if sys.platform == 'win32':
                font_path = os.path.join('C:\\Windows\\Fonts', font_file)
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    c.setFont(font_name, 12)
                    c.drawString(70, y_position, f'成功注册并使用 {font_name} 字体')
                else:
                    c.setFont('Helvetica', 12)
                    c.drawString(70, y_position, f'未找到 {font_name} 字体文件')
            else:
                c.setFont('Helvetica', 12)
                c.drawString(70, y_position, f'非Windows系统，跳过 {font_name} 字体注册')
        except Exception as e:
            c.setFont('Helvetica', 12)
            c.drawString(70, y_position, f'注册 {font_name} 字体时出错: {str(e)}')
        y_position -= 20

    # 保存PDF
    c.save()
    print(f'测试PDF已保存到: {pdf_path}')
    if os.path.exists(pdf_path):
        print(f'PDF文件已成功创建，大小: {os.path.getsize(pdf_path)/1024:.2f} KB')
    else:
        print('PDF文件创建失败')

if __name__ == '__main__':
    test_chinese_fonts()