import requests

# 测试服务器响应
def test_server_response():
    try:
        # 访问服务器根路径
        response = requests.get('http://localhost:5000')
        print(f'服务器响应状态码: {response.status_code}')
        print(f'服务器响应内容长度: {len(response.text)} 字符')
        
        # 尝试访问生成报告接口
        report_response = requests.post('http://localhost:5000/generate_report', json={'position': '前端开发工程师'})
        print(f'生成报告接口响应状态码: {report_response.status_code}')
        print(f'生成报告接口响应内容: {report_response.text}')
    except Exception as e:
        print(f'测试过程中出错: {str(e)}')

if __name__ == '__main__':
    test_server_response()