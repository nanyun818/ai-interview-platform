import requests
import json
import socket

# 检查端口是否开放
def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        result = sock.connect_ex((host, port))
        return result == 0
    finally:
        sock.close()

url = 'http://localhost:5000/chat'
headers = {'Content-Type': 'application/json'}
data = {'message': '你好'}

host = 'localhost'
port = 5000

# 检查端口是否开放
if check_port(host, port):
    print(f'端口 {port} 是开放的')
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f'状态码: {response.status_code}')
        print(f'响应内容: {response.text}')
    except Exception as e:
        print(f'请求错误: {str(e)}')
else:
    print(f'端口 {port} 是关闭的，无法连接到服务器')

# 尝试获取更多信息
try:
    # 查看本地IP地址
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f'本地IP地址: {ip_address}')
    # 尝试使用IP地址连接
    if check_port(ip_address, port):
        print(f'使用IP地址 {ip_address} 可以连接到端口 {port}')
        url_ip = f'http://{ip_address}:{port}/chat'
        response = requests.post(url_ip, headers=headers, json=data)
        print(f'使用IP地址的状态码: {response.status_code}')
        print(f'使用IP地址的响应内容: {response.text}')
    else:
        print(f'无法使用IP地址 {ip_address} 连接到端口 {port}')
except Exception as e:
    print(f'获取IP信息错误: {str(e)}')