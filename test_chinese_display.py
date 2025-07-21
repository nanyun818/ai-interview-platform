from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 尝试注册中文字体
def register_chinese_fonts():
    fonts_to_register = [
        ('SimHei', 'simhei.ttf'),
        ('SimSun', 'simsun.ttc')
    ]

    registered_fonts = []
    for font_name, font_file in fonts_to_register:
        try:
            # 检查Windows字体目录
            font_path = os.path.join('C:\Windows\Fonts', font_file)
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                registered_fonts.append(font_name)
                print(f'成功注册字体: {font_name}')
            else:
                print(f'未找到字体文件: {font_path}')
        except Exception as e:
            print(f'注册字体时出错: {font_name}, 错误: {str(e)}')

    print(f'成功注册的字体列表: {registered_fonts}')
    return registered_fonts

# 生成测试PDF
def generate_test_pdf():
    # 注册字体
    registered_fonts = register_chinese_fonts()

    # 创建PDF文档
    c = canvas.Canvas('test_chinese_display.pdf', pagesize=letter)
    width, height = letter

    # 设置字体
    font_name = 'SimHei' if 'SimHei' in registered_fonts else ('SimSun' if 'SimSun' in registered_fonts else 'Arial')
    print(f'使用字体: {font_name}')

    # 标题
    c.setFont(font_name, 24)
    c.drawCentredString(width/2, height-50, '中文显示测试')

    # 测试文本
    c.setFont(font_name, 12)
    c.drawString(50, height-100, '这是一段测试中文显示的文本。')
    c.drawString(50, height-120, '如果您能看到这段文字，说明中文显示正常。')
    c.drawString(50, height-140, '测试字体: ' + font_name)

    # 保存PDF
    c.save()
    print('PDF文件已保存为 test_chinese_display.pdf')

if __name__ == '__main__':
    generate_test_pdf()