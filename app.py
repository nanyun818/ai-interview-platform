import os
import logging
import json
import time
import requests
import websocket
import uuid
import sys
import datetime
from io import BytesIO
import cv2
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 初始化Flask应用
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)


# 存储分享链接令牌
share_tokens = {}

# 讯飞星火大模型 API 密钥
XINGHUO_API_KEY = '9616d55df7405c152285fcfeaa9c5e54'
XINGHUO_API_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')
    
    headers = {
        "Authorization": f"Bearer {XINGHUO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": message
    }
    
    try:
        response = requests.post(XINGHUO_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/video', methods=['POST'])
def video_process():
    try:
        # 这里可以添加视频处理逻辑
        # 示例：读取视频帧
        file = request.files['video']
        file.save('temp_video.mp4')
        cap = cv2.VideoCapture('temp_video.mp4')
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # 处理视频帧
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.close()
        cv2.destroyAllWindows()
        return jsonify({"status": "Video processed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_ai_summary(prompt):
    """调用星火大模型API生成面试总结"""
    import websocket
    import json
    import base64
    import hashlib
    import hmac
    import ssl
    from datetime import datetime
    from time import mktime
    from wsgiref.handlers import format_date_time
    from urllib.parse import urlencode, urlparse
    import os
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # 从环境变量获取API密钥，如果不存在则使用默认值
    # 讯飞星火大模型认证信息
    GPT_API_KEY = os.environ.get('XINGHUO_GPT_API_KEY', '9616d55df7405c152285fcfeaa9c5e54')
    GPT_API_SECRET = os.environ.get('XINGHUO_GPT_API_SECRET', 'ODExNTk4ZmRlMWJjMzFlYmU2NGNhNjEw')
    GPT_APPID = os.environ.get('XINGHUO_GPT_APPID', '73c06b9a')
    GPT_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'

    # 讯飞星火实时听写功能认证信息
    ASR_API_KEY = os.environ.get('XINGHUO_ASR_API_KEY', '6304d19fe686af9213246de50161e0da')
    ASR_APPID = os.environ.get('XINGHUO_ASR_APPID', '73c06b9a')

    # 检查API密钥是否存在
    if not GPT_API_KEY or not GPT_API_SECRET or not GPT_APPID:
        logger.error('讯飞星火大模型API密钥、密钥或APPID缺失')
        return '总结生成失败: 讯飞星火大模型API密钥、密钥或APPID缺失'

    class Ws_Param(object):
        def __init__(self, gpt_api_key, gpt_api_secret, gpt_url):
            self.APIKey = gpt_api_key
            self.APISecret = gpt_api_secret
            self.host = urlparse(gpt_url).netloc
            self.path = urlparse(gpt_url).path
            self.gpt_url = gpt_url

        def create_url(self):
            now = datetime.now()
            date = format_date_time(mktime(now.timetuple()))
            signature_origin = f"host: {self.host}\ndate: {date}\nGET {self.path} HTTP/1.1"
            signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'), digestmod=hashlib.sha256).digest()
            signature_sha_base64 = base64.b64encode(signature_sha).decode('utf-8')
            authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
            authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
            v = {
                "authorization": authorization,
                "date": date,
                "host": self.host
            }
            url = self.gpt_url + '?' + urlencode(v)
            logger.info(f'ws_url: {url}')
            return url

    # 构建请求参数，完全对齐 DEMO
    parameter = {
        "header": {
            "app_id": GPT_APPID,
            "uid": str(uuid.uuid4())  # 可选，建议加
        },
        "parameter": {
            "chat": {
                "domain": "generalv3.5",
                "temperature": 0.5,
                "max_tokens": 1024
            }
        },
        "payload": {
            "message": {
                "text": [
                    {"role": "system", "content": "你现在是AI面试官，请根据岗位和面试内容给出专业总结。"},
                    {"role": "user", "content": prompt}
                ]
            }
        }
    }

    result = []
    error_msg = None
    finished = False

    def on_error(ws, error):
        nonlocal error_msg, finished
        logger.error(f"### error: {error}")
        error_msg = str(error)
        finished = True

    def on_close(ws, close_status_code, close_msg):
        nonlocal finished
        logger.info("### closed ###")
        finished = True

    def on_open(ws):
        def run(*args):
            ws.send(json.dumps(parameter))
        import _thread as thread
        thread.start_new_thread(run, (ws,))

    def on_message(ws, message):
        nonlocal result, finished, error_msg
        try:
            data = json.loads(message)
            code = data['header']['code']
            if code != 0:
                logger.error(f'请求错误: {code}, {data}')
                error_msg = f'请求错误: {code}, {data}'
                ws.close()
                finished = True
                return
            # 兼容不同返回结构
            if 'payload' in data and 'choices' in data['payload']:
                choices = data["payload"]["choices"]
                if isinstance(choices, dict):
                    status = choices.get("status")
                    content = choices.get("text", "")
                    if content:
                        result.append(content)
                elif isinstance(choices, list):
                    for c in choices:
                        if 'content' in c:
                            result.append(c['content'])
                        if c.get('status') == 2:
                            finished = True
                            ws.close()
                            return
            # 兼容老结构
            if 'payload' in data and 'message' in data['payload']:
                text = data['payload']['message'].get('text', [])
                for t in text:
                    if 'content' in t:
                        result.append(t['content'])
            # 检查是否结束
            if 'payload' in data and 'choices' in data['payload']:
                status = data['payload']['choices'].get('status', None)
                if status == 2:
                    finished = True
                    ws.close()
        except Exception as e:
            logger.error(f'解析消息异常: {e}')
            error_msg = str(e)
            finished = True
            ws.close()

    wsParam = Ws_Param(GPT_API_KEY, GPT_API_SECRET, GPT_URL)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    import threading
    wst = threading.Thread(target=ws.run_forever, kwargs={'sslopt': {"cert_reqs": ssl.CERT_NONE}})
    wst.daemon = True
    wst.start()

    # 等待结果
    import time
    timeout = 30
    start_time = time.time()
    while not finished and (time.time() - start_time < timeout):
        time.sleep(0.1)
    ws.close()
    if error_msg:
        return f'总结生成失败: {error_msg}'
    if not result:
        return '总结生成失败: 未收到有效的响应内容'
    # 确保result中的所有元素都是字符串类型
    result = [str(item) for item in result]
    return '\n'.join(result)


def register_chinese_fonts():
    # 扩展字体列表，增加更多可能的中文字体
    fonts_to_register = [
        ('SimHei', 'simhei.ttf'),
        ('Microsoft YaHei', 'msyh.ttf'),
        ('Microsoft YaHei UI', 'msyhui.ttf'),
        ('Arial Unicode MS', 'arialuni.ttf'),
        ('SimSun', 'simsun.ttc'),
        ('FangSong', 'fangsong.ttf'),
        ('KaiTi', 'kaiti.ttf')
    ]

    registered_fonts = []
    for font_name, font_file in fonts_to_register:
        try:
            if sys.platform == 'win32':
                # 检查Windows字体目录
                font_path = os.path.join('C:\\Windows\\Fonts', font_file)
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    registered_fonts.append(font_name)
                    app.logger.info(f'成功注册字体: {font_name}')
                else:
                    app.logger.warning(f'未找到字体文件: {font_path}')
            else:
                app.logger.info(f'非Windows系统，跳过字体注册: {font_name}')
        except Exception as e:
            app.logger.error(f'注册字体时出错: {font_name}, 错误: {str(e)}')

    # 打印注册结果
    app.logger.info(f'成功注册的字体列表: {registered_fonts}')
    return registered_fonts

# 确保中文字体可用
def ensure_chinese_font_available():
    global registered_fonts
    if not registered_fonts:
        app.logger.warning('没有注册的字体，尝试重新注册...')
        registered_fonts = register_chinese_fonts()
    return registered_fonts

# 注册中文字体
registered_fonts = register_chinese_fonts()

def generate_interview_report(interview_data=None):
    app.logger.info(f'接收到的面试数据: {interview_data}')
    """生成面试报告PDF文件

    参数:
        interview_data: 包含面试信息的字典
    """
    try:
        # 确保中文字体可用
        ensure_chinese_font_available()
        app.logger.info('中文字体已确保可用')

        # 记录已注册的字体
        registered_fonts = pdfmetrics.getRegisteredFontNames()
        app.logger.info(f'当前已注册的字体: {registered_fonts}')
        
        # 检查是否有可用的中文字体
        has_chinese_font = any(font in registered_fonts for font in ['SimHei', 'SimSun', 'Microsoft YaHei'])
        app.logger.info(f'是否有可用的中文字体: {has_chinese_font}')

        # 设置字体 - 优先使用SimHei
        font_name = 'SimHei'
        if font_name not in registered_fonts:
            font_name = 'SimSun' if 'SimSun' in registered_fonts else 'Arial'
            app.logger.warning(f'首选字体 SimHei 未注册，使用替代字体: {font_name}')
        else:
            app.logger.info(f'使用字体: {font_name}')
        
        app.logger.info(f'最终选择的字体: {font_name}')

        # 创建PDF文档
        app.logger.info('开始创建PDF文档...')
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        app.logger.info('PDF文档创建成功')
        width, height = letter

        # 标题
        app.logger.info('开始绘制标题...')
        c.setFont(font_name, 24)
        c.drawCentredString(width/2, height-50, 'AI面试评估报告')
        app.logger.info('标题绘制成功')

        # 基本信息
        c.setFont(font_name, 12)
        # 确保总是使用当前时间生成日期
        current_time = datetime.datetime.now()
        app.logger.info(f'当前系统时间: {current_time}')
        c.drawString(50, height-100, f'生成日期: {current_time.strftime("%Y-%m-%d %H:%M:%S")}')

        # 候选人信息
        if interview_data:
              candidate_name = interview_data.get('candidate_name', '匿名候选人')
              # 确保正确获取岗位信息
              interview_position = interview_data.get('position', '未知岗位')
              app.logger.info(f'使用的面试岗位: {interview_position}')
              interview_duration = interview_data.get('duration', '30分钟')
        else:
              candidate_name = '匿名候选人'
              interview_position = '未知岗位'
              interview_duration = '30分钟'

        # 强制使用传入的岗位信息（如果有）
        # 确保正确获取岗位信息，优先使用position字段，兼容其他可能的字段名
        # 检查更多可能的岗位信息字段
        interview_position = interview_data.get('position', interview_data.get('job_title', interview_data.get('position_name', interview_data.get('selected_position', interview_data.get('job_position', '未知岗位')))))
        app.logger.info(f'interview_data keys: {interview_data.keys()}')
        app.logger.info(f'最终使用的岗位信息: {interview_position}')
        if interview_position == '未知岗位':
            app.logger.error('面试数据中未找到有效的岗位信息字段，请检查前端传递参数，可能的字段名: position, job_title, position_name, selected_position, job_position')

        app.logger.info('开始绘制候选人信息...')
        c.drawString(50, height-120, f'候选人姓名: {candidate_name}')
        c.drawString(50, height-140, f'面试岗位: {interview_position}')
        c.drawString(50, height-160, f'面试时长: {interview_duration}')
        app.logger.info('候选人信息绘制成功')

        # 评分部分
        scores = {
            '专业知识': 90,
            '沟通表达': 80,
            '问题解决': 85,
            '团队协作': 82,
            '创新思维': 88
        }

        if interview_data and 'scores' in interview_data:
            scores = interview_data['scores']

        # 计算综合评分
        app.logger.info('开始计算综合评分...')
        total_score = sum(scores.values()) / len(scores)
        app.logger.info(f'综合评分: {total_score:.1f}')

        # 绘制综合评分
        app.logger.info('开始绘制综合评分...')
        c.setFont(font_name, 16)
        c.drawString(50, height-190, f'综合评分: {total_score:.1f}/100')
        app.logger.info('综合评分绘制成功')

        # 绘制各维度评分
        y_position = height - 230
        for category, score in scores.items():
            c.setFont(font_name, 12)
            c.drawString(50, y_position, f'{category}: {score}分')
            # 绘制评分条
            c.rect(150, y_position - 5, 300, 10, fill=False)
            c.rect(150, y_position - 5, 300 * (score / 100), 10, fill=True)
            y_position -= 30
        app.logger.info('各维度评分绘制成功')
    except Exception as e:
        app.logger.error(f'PDF绘制过程中发生错误: {str(e)}')
        raise

    # 面试总结 [暂时注释掉]
    # app.logger.info('开始准备面试总结提示词...')
    # # 获取面试内容并添加到prompt中
    # interview_content = interview_data.get('interview_content', '未提供面试内容')
    # prompt = f"你现在需要对候选人的面试表现进行总结。候选人的基本信息如下：\n姓名：{candidate_name}\n应聘岗位：{interview_position}\n面试时长：{interview_duration}\n\n面试问答内容：\n{interview_content}\n\n请基于以上信息，对候选人的表现进行总结评估。评估应包括以下几个方面：\n1. 技术能力评估（针对{interview_position}岗位所需技能）\n2. 项目经验分析\n3. 综合素质评价\n4. 岗位匹配度分析（与{interview_position}岗位的匹配程度）\n5. 建议录用结论\n\n特别注意：必须严格基于提供的{interview_position}岗位信息和面试内容进行分析，不得假设其他岗位。"
    # app.logger.info('提示词准备完成')
    # # 调用星火大模型API生成总结
    # app.logger.info('开始调用大模型生成总结...')
    # try:
    #     summary = generate_ai_summary(prompt)
    #     app.logger.info(f'大模型返回的总结: {summary}')
    #     # 确保summary是字符串类型
    #     if not isinstance(summary, str):
    #         summary = str(summary)
    #     # 检查summary是否为空
    #     if not summary or summary.strip() == '':
    #         summary = '总结生成失败: 未收到有效的响应内容'
    # except Exception as e:
    #     app.logger.error(f'调用大模型生成总结时出错: {str(e)}')
    #     summary = f'总结生成失败: {str(e)}'

    #     app.logger.info('开始绘制面试总结...')
    #     c.setFont(font_name, 14)
    #     c.drawString(50, y_position - 20, '面试总结:')
    #     c.setFont(font_name, 12)

    #     # 使用Paragraph处理自动换行
    #     style = getSampleStyleSheet()['Normal']
    #     style.fontName = font_name  # 确保继承主字体
    #     style.fontSize = 12
    #     style.leading = 15
    #     
    #     summary_paragraph = Paragraph(summary, style)
    #     summary_paragraph.wrapOn(c, width-100, height)
    #     summary_paragraph.drawOn(c, 50, y_position - 40)
    #     app.logger.info('面试总结绘制成功')

        # 保存PDF
        c.save()

        # 移动到缓冲区开头
        buffer.seek(0)

        return buffer

    except Exception as e:
        app.logger.error(f'生成报告时出错: {str(e)}')
        return None

@app.route('/generate_report', methods=['POST'])
def generate_report():
    try:
        app.logger.info('开始生成新的面试报告...')
        # 确保正确解析JSON数据
        if request.is_json:
            interview_data = request.get_json()
            app.logger.info(f'通过request.get_json()获取到的面试数据: {interview_data}')
        else:
            # 尝试手动解析JSON
            try:
                interview_data = json.loads(request.data)
                app.logger.info(f'通过手动解析获取到的面试数据: {interview_data}')
            except json.JSONDecodeError:
                app.logger.error('无效的JSON格式')
                return jsonify({'error': '无效的JSON格式'}), 400
        
        # 验证必要的面试数据
        if not interview_data:
            app.logger.error('未提供面试数据')
            return jsonify({'error': '未提供面试数据'}), 400
        if 'position' not in interview_data:
            app.logger.error('面试数据中缺少职位信息')
            return jsonify({'error': '面试数据中缺少职位信息'}), 400
        
        # 确保岗位信息被正确传递
        app.logger.info(f'面试数据中的岗位信息: {interview_data["position"]}')
        # 验证岗位信息是否正确传递
        app.logger.debug(f'完整面试数据: {interview_data}')
        buffer = generate_interview_report(interview_data)
        
        if buffer:
            # 将报告保存到文件
            report_path = os.path.join(app.root_path, 'interview_report.pdf')
            with open(report_path, 'wb') as f:
                f.write(buffer.getvalue())
            
            app.logger.info(f'报告已成功生成: {report_path}')
            return jsonify({'status': 'success', 'message': '报告已成功生成', 'report_path': report_path})
        
        # 如果buffer为空，返回错误
        app.logger.error('生成报告缓冲区失败')
        return jsonify({'error': '报告生成失败，无法创建PDF内容'}), 500
    except Exception as e:
        app.logger.error(f'生成报告时出错: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/download_report')
def download_report():
    app.logger.info(f'Download attempt - app root path: {app.root_path}')
    report_path = os.path.join(app.root_path, 'interview_report.pdf')
    app.logger.info(f'Download attempt - checking report path: {report_path}')
    if not os.path.exists(report_path):
            app.logger.error(f'Report not found at: {report_path}')
            return jsonify({'error': 'Report not found. Please generate the report first through the interview process.'}), 404
    return send_file(report_path, as_attachment=True, download_name='interview_report.pdf')

@app.route('/generate_share_link', methods=['GET'])
def generate_share_link():
    token = str(uuid.uuid4())
    share_tokens[token] = {'created_at': datetime.datetime.now()}
    share_url = f"http://localhost:5001/share/{token}"
    return jsonify({'share_url': share_url})

@app.route('/share/<token>')
def share_interview(token):
    if token in share_tokens:
        return send_from_directory(os.getcwd(), 'index.html')
    else:
        return "无效或已过期的分享链接", 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)