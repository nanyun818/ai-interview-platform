import requests
import time
import json
import os
import shutil
import logging
import requests
import socket

def check_server():
    """检查服务器是否可达"""
    try:
        # 尝试连接服务器
        with socket.create_connection(('127.0.0.1', 5001), timeout=2) as s:
            return True
    except:
        return False

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_download_report():
    logger.info('开始测试下载报告功能...')
    
    # 检查服务器是否可达
    if not check_server():
        logger.error('服务器不可达，请确保服务器正在运行')
        return
    
    # 准备测试数据
    test_data = {
        'position': '后端开发工程师',
        'candidate_name': '测试候选人',
        'duration': '45分钟',
        'scores': {
            '专业知识': 90,
            '沟通表达': 80,
            '问题解决': 85,
            '团队协作': 82,
            '创新思维': 88
        }
    }
    
    # 设置请求头
    headers = {'Content-Type': 'application/json'}
    
    logger.info(f'Sending POST request to http://localhost:5001/generate_report with data: {test_data}')
    logger.info(f'Headers: {headers}')
    
    # 发送POST请求生成报告
    try:
        response = requests.post('http://localhost:5001/generate_report', json=test_data, headers=headers, timeout=10)
        
        logger.info(f'Response status code: {response.status_code}')
        logger.info(f'Response content: {response.text}')
        
        if response.status_code == 200:
            logger.info('报告生成成功，开始下载...')
            # 检查报告文件是否存在
            # 使用原始字符串避免转义序列问题
            report_path = r'E:\ai-interview-platform\interview_report.pdf'
            logger.info(f'检查报告文件是否存在: {report_path}')
            if os.path.exists(report_path):
                logger.info(f'报告文件存在，大小: {os.path.getsize(report_path)} 字节')
            else:
                logger.warning('报告文件不存在')
            # 等待1秒确保报告已保存
            time.sleep(1)
            # 下载报告
            download_response = requests.get('http://localhost:5001/download_report')
            if download_response.status_code == 200:
                logger.info('报告下载成功！')
                with open('downloaded_report.pdf', 'wb') as f:
                    f.write(download_response.content)
                logger.info('报告已保存为 downloaded_report.pdf')
            else:
                logger.error(f'下载报告失败，状态码: {download_response.status_code}')
                logger.error(f'错误信息: {download_response.text}')
        else:
            logger.error(f'报告生成失败: {response.status_code} {response.text}')
    except Exception as e:
        logger.error(f'发送请求时出错: {str(e)}')
        # 打印异常堆栈
        import traceback
        traceback.print_exc()
        
    # 清理生成的报告文件
    if os.path.exists('downloaded_report.pdf'):
        try:
            os.remove('downloaded_report.pdf')
            logger.info('已删除测试文件: downloaded_report.pdf')
        except Exception as e:
            logger.error(f'无法删除测试文件: {str(e)}')
    logger.info('测试完成')

if __name__ == '__main__':
    test_download_report()