import requests

# 测试服务器是否正常响应
try:
    response = requests.get('http://localhost:8000')
    print(f'服务器响应状态码: {response.status_code}')
    print(f'响应内容长度: {len(response.text)} 字符')

    # 测试聊天API
    chat_response = requests.post('http://localhost:8000/chat', json={'message': '测试消息', 'position': 'frontend-developer'})
    print(f'聊天API响应状态码: {chat_response.status_code}')
    print(f'聊天API响应内容: {chat_response.text}')
except Exception as e:
    print(f'测试失败: {e}')