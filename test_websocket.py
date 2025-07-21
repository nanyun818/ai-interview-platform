import websocket
# coding: utf-8
import _thread as thread
import base64
import hashlib
import hmac
import json
import ssl
import logging
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from urllib.parse import urlparse
from wsgiref.handlers import format_date_time
import websocket

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Ws_Param(object):
    # 初始化
    def __init__(self, APIKey, APISecret, gpt_url):
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    logger.error(f"WebSocket错误: {error}")


# 收到websocket关闭的处理
def on_close(ws, close_status_code, close_msg):
    logger.info("WebSocket连接已关闭")


# 收到websocket连接建立的处理
def on_open(ws):
    logger.info("WebSocket连接已建立")
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(parameter)
    # 发送请求参数
    ws.send(data)
    logger.info("已发送请求参数")


# 收到websocket消息的处理
def on_message(ws, message):
    try:
        data = json.loads(message)
        logger.debug(f"收到消息: {data}")
        code = data['header']['code']
        if code != 0:
            logger.error(f'请求错误: {code}, {data}')
            ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            logger.info(f"收到回复: {content}")
            if status == 2:
                logger.info("会话已结束")
                ws.close()
    except Exception as e:
        logger.error(f"处理消息时出错: {str(e)}")

# WebSocket 请求的参数
parameter = {
  "payload": {
      "message": {
          "text": [
              {
                  "role": "system",
                  "content": "你是一个ai面试官 需要复制帮助我完成面试的问题问答。以及改进建议"
              },
              {
                  "role": "user",
                  "content": "你好"
              }
          ]
      }
  },
  "parameter": {
      "chat": {
          "max_tokens": 4096,
          "domain": "generalv3.5",
          "top_k": 4,
          "temperature": 0.5
      }
  },
  "header": {
      "app_id": "73c06b9a"
  }
}


def main(api_secret, api_key, gpt_url):
    try:
        logger.info(f"开始连接到 {gpt_url}")
        wsParam = Ws_Param(api_key, api_secret, gpt_url)
        websocket.enableTrace(False)
        wsUrl = wsParam.create_url()
        logger.debug(f"生成的URL: {wsUrl}")
        ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    except Exception as e:
        logger.error(f"连接过程中出错: {str(e)}")


if __name__ == "__main__":
    # 星火认知大模型调用秘钥信息
    API_KEY = '9616d55df7405c152285fcfeaa9c5e54'
    API_SECRET = 'ODExNTk4ZmRlMWJjMzFlYmU2NGNhNjEw'
    GPT_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'

    logger.info("开始运行WebSocket测试")
    main(
        api_secret=API_SECRET,
        api_key=API_KEY,
        gpt_url=GPT_URL
    )