from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 尝试注册中文字体
try:
    # 尝试注册SimHei字体
    pdfmetrics.registerFont(TTFont('SimHei', 'C:\\Windows\\Fonts\\simhei.ttf'))
    print('成功注册字体: SimHei')
except Exception as e:
    print(f'注册字体SimHei失败: {str(e)}')

try:
    # 尝试注册SimSun字体
    pdfmetrics.registerFont(TTFont('SimSun', 'C:\\Windows\\Fonts\\simsun.ttc'))
    print('成功注册字体: SimSun')
except Exception as e:
    print(f'注册字体SimSun失败: {str(e)}')

# 查看已注册的字体
registered_fonts = pdfmetrics.getRegisteredFontNames()
print(f'已注册的字体列表: {registered_fonts}')

# 创建PDF文档
buffer = open('chinese_test.pdf', 'wb')
c = canvas.Canvas(buffer, pagesize=letter)
width, height = letter

# 选择字体
font_name = 'SimHei' if 'SimHei' in registered_fonts else ('SimSun' if 'SimSun' in registered_fonts else 'Arial')
print(f'使用字体: {font_name}')

# 绘制中文文本
c.setFont(font_name, 24)
c.drawCentredString(width/2, height-50, '中文测试文档')

c.setFont(font_name, 16)
c.drawString(50, height-100, '这是一个测试文档，用于检查中文显示效果。')
c.drawString(50, height-130, '测试内容:')
c.drawString(70, height-160, '1. 中文标题显示')
c.drawString(70, height-190, '2. 中文正文显示')
c.drawString(70, height-220, '3. 中文列表显示')

# 保存PDF
c.save()
buffer.close()

print('PDF文件已保存为 chinese_test.pdf')

# 尝试打开文件
try:
    os.startfile('chinese_test.pdf')
    print('已尝试打开PDF文件')
except Exception as e:
    print(f'无法打开文件: {str(e)}')