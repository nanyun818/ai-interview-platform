import logging
import os
import time
import uuid
import websocket
import json
import hmac
import hashlib
import base64
import urllib.parse

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SparkChainTest:
    def __init__(self):
        # 从环境变量获取API密钥
        self.XINGHUO_API_KEY = os.environ.get('XINGHUO_API_KEY', '9616d55df7405c152285fcfeaa9c5e54')
        self.XINGHUO_API_SECRET = os.environ.get('XINGHUO_API_SECRET', 'ODExNTk4ZmRlMWJjMzFlYmU2NGNhNjEw')
        self.XINGHUO_APPID = os.environ.get('XINGHUO_APPID', '73c06b9a')
        self.HOST = 'spark-api.xf-yun.com'
        self.PATH = '/v3.5/chat'
        self.DOMAIN = 'generalv3.5'
        self.URL = f'wss://{self.HOST}{self.PATH}'

    def test_connection(self):
        try:
            logger.info(f'使用的API密钥: {self.XINGHUO_API_KEY[:5]}...')
            logger.info(f'使用的API密钥长度: {len(self.XINGHUO_API_KEY)}')
            logger.info(f'使用的API密钥Secret长度: {len(self.XINGHUO_API_SECRET)}')
            logger.info(f'使用的AppID: {self.XINGHUO_APPID}')
            logger.info(f'使用的Domain: {self.DOMAIN}')
            logger.info(f'使用的URL: {self.URL}')

            # 检查API_SECRET长度
            if len(self.XINGHUO_API_SECRET) != 32:
                logger.warning(f'API_SECRET长度不是32位，而是{len(self.XINGHUO_API_SECRET)}位，可能不正确')

            # 生成 RFC1123 格式的时间
            date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
            request_line = f'GET {self.PATH} HTTP/1.1'
            signature_origin = f'host: {self.HOST}\ndate: {date}\n{request_line}'
            logger.debug(f'签名原始字符串:\n{signature_origin}')

            # 生成签名
            try:
                signature_sha = hmac.new(self.XINGHUO_API_SECRET.encode('utf-8'), signature_origin.encode('utf-8'), hashlib.sha256).digest()
                signature = base64.b64encode(signature_sha).decode('utf-8')
                logger.debug(f'生成的签名: {signature}')
            except Exception as e:
                logger.error(f'生成签名时出错: {str(e)}')
                return f'测试失败: 生成签名时出错 - {str(e)}'

            # 生成授权
            try:
                authorization_origin = f'api_key="{self.XINGHUO_API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
                authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
                logger.debug(f'生成的授权: {authorization}')
            except Exception as e:
                logger.error(f'生成授权时出错: {str(e)}')
                return f'测试失败: 生成授权时出错 - {str(e)}'

            # 构建URL
            try:
                ws_url = f"wss://{self.HOST}{self.PATH}?authorization={urllib.parse.quote(authorization)}&date={urllib.parse.quote(date)}&host={self.HOST}"
                logger.info(f'最终WebSocket URL: {ws_url[:150]}...')
            except Exception as e:
                logger.error(f'构建URL时出错: {str(e)}')
                return f'测试失败: 构建URL时出错 - {str(e)}'

            # 建立WebSocket连接
            logger.info('尝试连接大模型API...')
            try:
                ws = websocket.create_connection(ws_url, timeout=10)
                logger.info('WebSocket连接成功')
            except websocket.WebSocketException as e:
                logger.error(f'WebSocket连接失败: {str(e)}')
                if '401' in str(e):
                    return '测试失败: 权限不足或API密钥无效，请检查您的API密钥是否正确且具有足够的权限\n错误详情: HMAC签名不匹配，可能是API密钥或Secret不正确\n请确认您的API密钥和Secret是否来自讯飞星火大模型控制台，并且没有过期'
                elif 'Connection refused' in str(e):
                    return '测试失败: 连接被拒绝，请检查API URL是否正确或网络是否通畅'
                else:
                    return f'测试失败: WebSocket连接错误 - {str(e)}'

            # 构建请求参数
            payload = {
                'header': {
                    'app_id': self.XINGHUO_APPID,
                    'uid': str(uuid.uuid4())
                },
                'parameter': {
                    'chat': {
                        'domain': self.DOMAIN,
                        'temperature': 0.7,
                        'max_tokens': 1000
                    }
                },
                'payload': {
                    'message': {
                        'text': [{'role': 'user', 'content': '你好'}]
                    }
                }
            }

            # 发送数据
            try:
                ws.send(json.dumps(payload))
                logger.info('数据发送成功')
            except Exception as e:
                logger.error(f'发送数据时出错: {str(e)}')
                ws.close()
                return f'测试失败: 发送数据时出错 - {str(e)}'

            # 接收数据
            result = ''
            timeout = time.time() + 30  # 设置30秒超时
            received_response = False
            retry_count = 0
            max_retries = 3
            finish = False

            while time.time() < timeout and not finish:
                try:
                    response = ws.recv()
                    received_response = True
                    logger.debug(f'收到原始响应: {response[:100]}...')
                    try:
                        response_data = json.loads(response)
                        logger.debug(f'解析后的响应: {str(response_data)[:100]}...')
                        # 检查响应头
                        header = response_data.get('header', {})
                        logger.debug(f'响应头: {header}')
                        # 检查是否有错误
                        if header.get('code') != 0:
                            logger.error(f'响应出错: 代码={header.get("code")}, 消息={header.get("message")}')
                            return f'测试失败: 大模型返回错误 - 代码={header.get("code")}, 消息={header.get("message")}'
                        # 检查是否是最后一条消息
                        if header.get('status') == 2:
                            logger.info('收到最后一条消息')
                            finish = True
                        # 提取文本
                        if 'payload' in response_data:
                            payload = response_data['payload']
                            if 'choices' in payload:
                                choices = payload['choices']
                                logger.debug(f'choices类型: {type(choices)}, 内容: {str(choices)[:50]}...')
                                if isinstance(choices, dict):
                                    # 处理choices为字典的情况
                                    text = choices.get('text', [])
                                    if isinstance(text, list) and len(text) > 0:
                                        text_msg = text[0]
                                        content = text_msg.get('content', '')
                                        result += content
                                        logger.info(f'收到部分响应: {content[:30]}...')
                                    else:
                                        logger.warning(f'choices为字典但text不是有效的列表或为空: {str(text)[:50]}...')
                                elif isinstance(choices, list) and len(choices) > 0:
                                    # 处理choices为列表的情况
                                    choice_item = choices[0]
                                    content = choice_item.get('content', '')
                                    result += content
                                    logger.info(f'收到部分响应: {content[:30]}...')
                                else:
                                    logger.warning(f'choices不是有效的列表或字典: {str(choices)[:50]}...')
                            elif 'message' in payload:
                                text = payload['message'].get('text', [])
                                logger.debug(f'text类型: {type(text)}, 内容: {str(text)[:50]}...')
                                if isinstance(text, list) and len(text) > 0:
                                    text_msg = text[0]
                                    result += text_msg.get('content', '')
                                    logger.info(f'收到部分响应: {text_msg.get("content", "")[:30]}...')
                                else:
                                    logger.warning(f'text不是有效的列表或为空: {str(text)[:50]}...')
                            else:
                                logger.warning(f'未识别的payload格式: {str(payload)[:50]}...')
                        else:
                            logger.warning(f'响应中没有payload: {str(response_data)[:50]}...')
                    except json.JSONDecodeError as e:
                        logger.error(f'JSON解析错误: {str(e)}, 响应内容: {response[:50]}...')
                        # 尝试重新接收数据
                        retry_count += 1
                        if retry_count <= max_retries:
                            logger.warning(f'第{retry_count}次重试接收数据...')
                            continue
                        else:
                            logger.error(f'超过最大重试次数({max_retries})，停止尝试')
                            break
                except websocket.WebSocketTimeoutException:
                    logger.warning('WebSocket接收超时，继续等待...')
                    continue
                except Exception as e:
                    logger.error(f'接收数据异常: {type(e).__name__} - {str(e)}')
                    break

            if not received_response:
                logger.warning('未收到任何响应')
                return '测试失败: 未收到任何响应，请检查网络连接或API服务状态'

            ws.close()
            logger.info(f'大模型返回的结果: {result[:100]}...')
            return result if result else '测试失败: 未收到有效的响应内容'
        except json.JSONDecodeError as e:
            logger.error(f'JSON解析错误: {str(e)}')
            return f'测试失败: 响应解析错误 - {str(e)}'
        except Exception as e:
            logger.error(f'发生未知错误: {str(e)}')
            return f'测试失败: 未知错误 - {str(e)}'

def test_spark_connection():
    test = SparkChainTest()
    return test.test_connection()

if __name__ == '__main__':
    logger.info('开始测试讯飞星火大模型连接...')
    # 检查网络连接
    try:
        import socket
        # 尝试连接到百度主页
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(('www.baidu.com', 80))
        s.close()
        logger.info('网络连接正常')
    except Exception as e:
        logger.error(f'网络连接可能有问题: {str(e)}')
        print(f'警告: 网络连接可能有问题: {str(e)}')

    result = test_spark_connection()
    logger.info(f'测试结果: {result}')

    # 输出测试结果
    print(f'测试结果: {result}')
    print(f'测试结果: {result}')