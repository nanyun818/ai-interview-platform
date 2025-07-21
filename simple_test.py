from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 尝试注册中文字体
def register_fonts():
    font_list = [
        ('SimHei', 'simhei.ttf'),
        ('SimSun', 'simsun.ttc')
    ]
    registered = []
    for font_name, font_file in font_list:
        try:
            if os.name == 'nt':  # Windows系统
                font_path = os.path.join('C:\Windows\Fonts', font_file)
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    registered.append(font_name)
                    print(f'成功注册字体: {font_name}')
                else:
                    print(f'未找到字体文件: {font_path}')
            else:
                print('非Windows系统，跳过字体注册')
        except Exception as e:
            print(f'注册字体时出错: {font_name}, 错误: {str(e)}')
    return registered

# 测试中文字体
def test_font():
    # 注册字体
    registered_fonts = register_fonts()
    print(f'成功注册的字体: {registered_fonts}')

    # 创建PDF
    c = canvas.Canvas('test_font.pdf', pagesSize=letter)
    width, height = letter

    # 选择字体
    font_name = 'SimHei' if 'SimHei' in registered_fonts else ('SimSun' if 'SimSun' in registered_fonts else 'Arial')
    print(f'使用字体: {font_name}')

    # 绘制文本
    c.setFont(font_name, 24)
    c.drawString(50, height-50, '测试中文字体')

    c.setFont(font_name, 12)
    c.drawString(50, height-100, '这是一段测试文本，用于验证中文字体是否正确显示。')

    # 保存PDF
    c.save()
    print('PDF已保存到: test_font.pdf')

if __name__ == '__main__':
    test_font()