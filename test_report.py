import os
import sys
import unittest
import datetime
from app import app, generate_interview_report

class TestInterviewReport(unittest.TestCase):
    def setUp(self):
        # 设置测试环境
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.report_path = os.path.join(app.root_path, 'interview_report.pdf')
        # 确保测试前报告不存在
        if os.path.exists(self.report_path):
            os.remove(self.report_path)

    def test_generate_report_with_default_data(self):
        # 测试使用默认数据生成报告
        print(f'测试开始时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        with app.app_context():
            report_buffer = generate_interview_report()
            self.assertIsNotNone(report_buffer)
            # 保存报告到文件
            with open(self.report_path, 'wb') as f:
                f.write(report_buffer.getvalue())
            self.assertTrue(os.path.exists(self.report_path))
            print(f'成功生成默认报告: {self.report_path}')
            print(f'测试结束时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    def test_generate_report_with_custom_data(self):
        # 测试使用自定义数据生成报告
        custom_data = {
            'candidate_name': '张三',
            'interview_position': '高级AI工程师',
            'interview_duration': '60分钟',
            'scores': {
                '专业知识': 95,
                '沟通表达': 85,
                '问题解决': 90,
                '团队协作': 88,
                '创新思维': 92
            },
            'summary': '该候选人在专业知识方面表现卓越，特别是在深度学习和计算机视觉方面有深入的研究。沟通表达能力良好，能够清晰地描述复杂的技术问题。问题解决能力强，能够快速分析问题并提出有效的解决方案。团队协作能力出色，能够积极参与团队讨论并带领团队解决问题。创新思维突出，经常能够提出新颖的解决方案和想法。',
            'suggestions': [
                '1. 继续深入研究前沿的AI技术，保持技术的领先性',
                '2. 提高项目管理能力，学习如何规划和管理大型AI项目',
                '3. 加强团队领导能力的培养，学习如何带领团队实现目标',
                '4. 继续保持创新思维，同时学会如何将创新想法落地实现',
                '5. 加强与业务部门的沟通，了解业务需求，更好地发挥AI技术的价值'
            ]
        }
        with app.app_context():
            report_buffer = generate_interview_report(custom_data)
            self.assertIsNotNone(report_buffer)
            # 保存报告到文件
            with open(self.report_path, 'wb') as f:
                f.write(report_buffer.getvalue())
            self.assertTrue(os.path.exists(self.report_path))
            print(f'成功生成自定义报告: {self.report_path}')

    def tearDown(self):
        # 保留报告文件以便检查
        pass

if __name__ == '__main__':
    unittest.main()