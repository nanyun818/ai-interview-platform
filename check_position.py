import PyPDF2
import os
import sys

# 检查文件是否存在
report_path = os.path.join(os.getcwd(), 'interview_report.pdf')
# 确保删除旧的报告文件
if os.path.exists(report_path):
    os.remove(report_path)
    print(f'已删除旧报告文件: {report_path}')

print('尝试生成新报告...')
# 尝试导入generate_interview_report函数
try:
    # 导入app模块
    import app
    # 创建测试数据
    test_data = {
        'candidate_name': '测试候选人',
        'position': '前端开发工程师',  # 设置明确的岗位信息
        'duration': '45分钟'
    }
    print(f'测试数据: {test_data}')
    # 生成报告
    buffer = app.generate_interview_report(test_data)
    if buffer:
        # 保存报告
        with open(report_path, 'wb') as f:
            f.write(buffer.getvalue())
        print(f'报告已生成: {report_path}')
    else:
        print('生成报告失败')
except Exception as e:
    print(f'生成报告时出错: {str(e)}')

# 检查报告是否存在
if not os.path.exists(report_path):
    print('报告文件不存在')
    exit()

# 读取PDF文件
try:
    with open(report_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        # 读取第一页
        if len(reader.pages) > 0:
            page = reader.pages[0]
            text = page.extract_text()
            print('PDF第一页内容:')
            print(text)
            # 检查是否包含岗位信息
            if '面试岗位:' in text:
                print('\n找到岗位信息:')
                # 提取岗位信息
                position_start = text.find('面试岗位:') + len('面试岗位:')
                position_end = text.find('\n', position_start)
                if position_end != -1:
                    position = text[position_start:position_end].strip()
                    print(f'岗位名称: {position}')
                else:
                    print('无法提取完整的岗位信息')
            else:
                print('未找到岗位信息')
        else:
            print('PDF文件为空')
except Exception as e:
    print(f'读取PDF文件时出错: {str(e)}')