import requests
import json

# 测试生成报告接口，确保岗位信息被正确使用
print('测试生成报告接口...')

test_data = {
    'candidate_name': '测试候选人',
    'position': '前端开发工程师',
    'duration': '45分钟',
    'scores': {
        '专业知识': 90,
        '沟通表达': 85,
        '问题解决': 88,
        '团队协作': 82,
        '创新思维': 92
    }
}

try:
    response = requests.post('http://localhost:5000/generate_report', json=test_data)
    print(f'响应状态码: {response.status_code}')
    print(f'响应内容: {response.text}')
    
    # 尝试下载报告
    if response.status_code == 200:
        print('\n尝试下载报告...')
        download_response = requests.get('http://localhost:5000/download_report')
        print(f'下载响应状态码: {download_response.status_code}')
        if download_response.status_code == 200:
            print('报告下载成功！')
        else:
            print('报告下载失败。')
except Exception as e:
    print(f'测试过程中出错: {str(e)}')