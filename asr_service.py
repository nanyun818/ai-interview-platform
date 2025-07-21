import os
import logging
import json
import base64
import hashlib
import hmac
import ssl
import websocket
import uuid
from datetime import datetime
from time import mktime
from urllib.parse import urlencode, urlparse
from wsgiref.handlers import format_date_time

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ASR_Param(object):
    def __init__(self, asr_api_key, asr_appid, asr_url):
        self.APIKey = asr_api_key
        self.AppID = asr_appid
        self.host = urlparse(asr_url).netloc
        self.path = urlparse(asr_url).path
        self.asr_url = asr_url

    def create_url(self):
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        
        # 拼接字符串
        signature_origin = f"host: {self.host}\ndate: {date}\nGET {self.path} HTTP/1.1"
        
        # 进行hmac-sha256加密
        signature_sha = hmac.new(self.APIKey.encode('utf-8'), signature_origin.encode('utf-8'),
                                digestmod=hashlib.sha256).digest()
        
        signature_sha_base64 = base64.b64encode(signature_sha).decode('utf-8')
        
        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
        
        # 组合鉴权参数
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        
        # 生成url
        url = self.asr_url + '?' + urlencode(v)
        logger.info(f'生成的ASR URL: {url}')
        return url

def generate_asr_result(audio_data):
    """调用讯飞星火听写API转换语音为文本"""
    # 从环境变量获取API密钥，如果不存在则使用默认值
    ASR_API_KEY = os.environ.get('XINGHUO_ASR_API_KEY', '6304d19fe686af9213246de50161e0da')
    ASR_APPID = os.environ.get('XINGHUO_ASR_APPID', '73c06b9a')
    ASR_URL = 'wss://rtasr.xfyun.cn/v1/ws'  # 讯飞星火听写功能的WebSocket URL
    
    # 检查API密钥是否存在
    if not ASR_API_KEY or not ASR_APPID:
        logger.error('讯飞星火听写API密钥或APPID缺失')
        return '听写失败: 讯飞星火听写API密钥或APPID缺失'
    
    # 构建请求参数
    parameter = {
        "header": {
            "app_id": ASR_APPID,
            "uid": str(uuid.uuid4())
        },
        "parameter": {
            "asr": {
                "domain": "iat",
                "language": "zh_cn",
                "accent": "mandarin",
                "format": "pcm",
                "sample_rate": 16000
            }
        }
    }
    
    result = []
    error_msg = None
    finished = False
    
    def on_error(ws, error):
        nonlocal error_msg, finished
        logger.error(f"ASR WebSocket错误: {error}")
        error_msg = str(error)
        finished = True
    
    def on_close(ws, close_status_code, close_msg):
        nonlocal finished
        logger.info("ASR WebSocket连接已关闭")
        finished = True
    
    def on_open(ws):
        def run(*args):
            # 发送参数
            ws.send(json.dumps(parameter))
            # 发送音频数据
            ws.send(audio_data)
            # 发送结束帧
            ws.send('')
        
        import _thread as thread
        thread.start_new_thread(run, ())
    
    def on_message(ws, message):
        nonlocal result, finished, error_msg
        try:
            data = json.loads(message)
            code = data['header']['code']
            if code != 0:
                logger.error(f'ASR请求错误: {code}, {data}')
                error_msg = f'ASR请求错误: {code}, {data}'
                ws.close()
                finished = True
                return
            
            # 处理听写结果
            if 'payload' in data and 'result' in data['payload']:
                asr_result = data['payload']['result']
                if 'text' in asr_result:
                    result.append(asr_result['text'])
                
                # 检查是否结束
                if asr_result.get('status') == 2:
                    finished = True
                    ws.close()
        except Exception as e:
            logger.error(f'解析ASR消息异常: {e}')
            error_msg = str(e)
            finished = True
            ws.close()
    
    # 创建ASR参数对象
    asrParam = ASR_Param(ASR_API_KEY, ASR_APPID, ASR_URL)
    
    # 生成WebSocket URL
    websocket.enableTrace(False)
    wsUrl = asrParam.create_url()
    
    # 创建WebSocket连接
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    
    # 启动WebSocket连接
    import threading
    wst = threading.Thread(target=ws.run_forever, kwargs={'sslopt': {"cert_reqs": ssl.CERT_NONE}})
    wst.daemon = True
    wst.start()
    
    # 等待结果
    import time
    timeout = 60  # 60秒超时
    start_time = time.time()
    while not finished and (time.time() - start_time < timeout):
        time.sleep(0.1)
    
    # 关闭连接
    ws.close()
    
    # 处理结果
    if error_msg:
        return f'听写失败: {error_msg}'
    if not result:
        return '听写失败: 未收到有效的听写结果'
    
    return ''.join(result)

# 示例用法
if __name__ == '__main__':
    import uuid
    # 这里只是演示，实际使用时需要提供真实的音频数据
    # 例如: with open('audio.pcm', 'rb') as f:
    #         audio_data = f.read()
    audio_data = b'this is audio data'
    result = generate_asr_result(audio_data)
    print(f'听写结果: {result}')