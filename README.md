# AI面试平台

## 项目简介
这是一个基于AI的面试评估平台，能够帮助企业更高效、更准确地评估候选人。平台通过集成多种AI技术，包括自然语言处理、计算机视觉等，为企业提供全方位的面试解决方案。

## 系统特色
1. **智能评估**：利用先进的AI模型对候选人的回答进行自动评分和总结
2. **多维度分析**：从专业知识、沟通表达、问题解决、团队协作、创新思维等多个维度评估候选人
3. **自动生成报告**：面试结束后自动生成详细的PDF评估报告
4. **岗位匹配度分析**：根据候选人的表现和岗位要求，分析其匹配程度
5. **视频面试支持**：支持视频面试，并对候选人的非语言行为进行分析
6. **分享功能**：生成可分享的面试报告链接

## 技术栈
- 后端：Python + Flask
- 前端：HTML + JavaScript
- AI模型：讯飞星火大模型
- PDF生成：ReportLab
- 视频处理：OpenCV
- 其他库：requests, websocket, uuid, datetime等

## 项目结构
```
e:\ai-interview-platform\
├── .venv\              # 虚拟环境
├── __pycache__\        # 编译缓存
├── app.py              # 主应用文件
├── asr_service.py      # 语音识别服务
├── cartoon-interview.svg # 卡通面试图标
├── check_env.py        # 环境检查脚本
├── check_file_modified.py # 文件修改检查
├── check_pdf_date.py   # PDF日期检查
├── check_pdf_font.py   # PDF字体检查
├── check_position.py   # 岗位检查
├── check_report.py     # 报告检查
├── chinese_test.pdf    # 中文测试PDF
├── demo.sln            # 演示解决方案
├── demo\               # 演示项目
├── download_report.py  # 下载报告脚本
├── generate_report.py  # 生成报告脚本
├── include\            # 头文件
├── index.html          # 首页
├── interview_report.pdf # 面试报告
├── libs\               # 库文件
├── requirements.txt    # 依赖包
├── simple_chinese_test.py # 简单中文测试
├── simple_test.py      # 简单测试
├── start_server.py     # 启动服务器脚本
├── test_api_key.py     # 测试API密钥
├── test_asr_api.py     # 测试ASR API
├── test_chat.py        # 测试聊天
├── test_chinese_display.pdf # 中文显示测试PDF
├── test_chinese_display.py # 中文显示测试
├── test_chinese_font.pdf # 中文字体测试PDF
├── test_chinese_font.py # 中文字体测试
├── test_download.py    # 测试下载
├── test_fix.py         # 测试修复
├── test_font.pdf       # 字体测试PDF
├── test_font_display.html # 字体显示测试
├── test_report.py      # 测试报告
├── test_server.py      # 测试服务器
├── test_server_response.py # 测试服务器响应
├── test_spark.py       # 测试星火模型
├── test_websocket.py   # 测试WebSocket
└── view_html.py        # 查看HTML
```

## 安装指南
1. 克隆仓库
   ```
   git clone https://github.com/nanyun818/ai-interview-platform.git
   cd ai-interview-platform
   ```

2. 创建虚拟环境
   ```
   python -m venv .venv
   ```

3. 激活虚拟环境
   - Windows
     ```
     .venv\Scripts\activate
     ```
   - macOS/Linux
     ```
     source .venv/bin/activate
     ```

4. 安装依赖
   ```
   pip install -r requirements.txt
   ```

5. 配置API密钥
   在代码中配置讯飞星火大模型的API密钥

## 使用说明
1. 启动服务器
   ```
   python start_server.py
   ```

2. 访问平台
   打开浏览器，访问 `http://localhost:5001`

3. 进行面试
   - 填写候选人信息和岗位信息
   - 进行面试问答
   - 系统会自动记录和分析面试过程

4. 生成报告
   面试结束后，系统会自动生成详细的PDF评估报告

5. 分享报告
   可以生成分享链接，分享给相关人员

## 贡献指南
1.  Fork 仓库
2.  创建特性分支
3.  提交更改
4.  推送到分支
5.  创建 Pull Request

## 许可证
本项目采用 MIT 许可证，详情请见 LICENSE 文件。

## 联系我们
如有任何问题或建议，请联系我们。

© 2025 AI面试平台 版权所有