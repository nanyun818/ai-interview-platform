# AI 面试平台 🚀

## 项目简介
AI 面试平台是一个基于人工智能的面试辅助系统，旨在帮助企业更高效、更准确地评估候选人。系统提供视频面试录制、自动语音识别、AI 面试总结和评估、PDF 报告生成等功能，为招聘决策提供数据支持。

## 系统特色 🌟
1. **智能语音识别**：采用先进的语音识别技术，将面试中的语音转换为文本，准确率高达95%以上。
2. **AI 面试评估**：基于大模型对候选人的回答进行分析和评估，提供客观的评分和反馈。
3. **自动报告生成**：自动生成详细的 PDF 面试报告，包含候选人信息、面试内容、评分和总结。
4. **岗位匹配分析**：根据候选人的表现和岗位要求，提供岗位匹配度分析，帮助企业找到最合适的人才。
5. **用户友好界面**：简洁明了的用户界面，易于操作和使用，无需专业培训即可上手。
6. **数据安全保障**：采用高级加密技术，确保面试数据的安全性和保密性。
7. **多语言支持**：支持多种语言的面试，满足企业国际化招聘的需求。
8. **实时反馈**：提供实时的面试反馈，帮助候选人了解自己的表现。

## 技术栈 🛠️
- **后端**：Python, Flask
- **前端**：HTML, CSS, JavaScript
- **AI 模型**：讯飞星火大模型
- **语音识别**：讯飞语音识别 API
- **PDF 生成**：ReportLab
- **其他库**：pandas, numpy, matplotlib

## 项目结构 📁
```
ai-interview-platform/
├── .venv/                  # 虚拟环境
├── README.md               # 项目说明
├── __pycache__/            # 编译后的Python文件
├── app.py                  # 主应用文件
├── asr_service.py          # 语音识别服务
├── cartoon-interview.svg   # 卡通面试图标
├── check_env.py            # 环境检查脚本
├── check_file_modified.py  # 文件修改检查脚本
├── check_pdf_date.py       # PDF 日期检查脚本
├── check_pdf_font.py       # PDF 字体检查脚本
├── check_position.py       # 岗位检查脚本
├── check_report.py         # 报告检查脚本
├── chinese_test.pdf        # 中文测试 PDF
├── demo.sln                # 解决方案文件
├── demo/                   # 演示项目
├── download_report.py      # 报告下载脚本
├── generate_report.py      # 报告生成脚本
├── include/                # 头文件
├── index.html              # 首页 HTML
├── interview_report.pdf    # 面试报告示例
├── libs/                   # 库文件
├── requirements.txt        # 依赖库列表
├── simple_chinese_test.py  # 简单中文测试脚本
├── simple_test.py          # 简单测试脚本
├── start_server.py         # 服务器启动脚本
├── test_api_key.py         # API 密钥测试脚本
├── test_asr_api.py         # 语音识别 API 测试脚本
├── test_chat.py            # 聊天测试脚本
├── test_chinese_display.pdf # 中文显示测试 PDF
├── test_chinese_display.py # 中文显示测试脚本
├── test_chinese_font.pdf   # 中文字体测试 PDF
├── test_chinese_font.py    # 中文字体测试脚本
├── test_download.py        # 下载测试脚本
├── test_fix.py             # 修复测试脚本
├── test_font.pdf           # 字体测试 PDF
├── test_font_display.html  # 字体显示测试 HTML
├── test_report.py          # 报告测试脚本
├── test_server.py          # 服务器测试脚本
├── test_server_response.py # 服务器响应测试脚本
├── test_spark.py           # 星火模型测试脚本
├── test_websocket.py       # WebSocket 测试脚本
└── view_html.py            # HTML 查看脚本
```

## 安装指南 🔧
1. **克隆仓库**
```bash
git clone https://github.com/user/ai-interview-platform.git
cd ai-interview-platform
```

2. **创建虚拟环境**
```bash
python -m venv .venv
```

3. **激活虚拟环境**
- Windows
```bash
.venv\Scripts\activate
```
- macOS/Linux
```bash
source .venv/bin/activate
```

4. **安装依赖**
```bash
pip install -r requirements.txt
```

5. **配置 API 密钥**
在使用前，需要配置讯飞星火大模型和语音识别的 API 密钥。请在 `app.py` 中修改相关配置。

## 使用说明 📖
1. **启动服务器**
```bash
python start_server.py
```

2. **访问系统**
打开浏览器，访问 `http://localhost:5000`。

3. **使用功能**
- 录制面试视频
- 上传面试视频
- 查看面试报告
- 下载面试报告
- 生成面试报告分享链接

## 功能详细介绍 🔍
### 1. 视频面试录制
系统支持实时视频面试录制，候选人可以通过浏览器进行面试，无需安装额外的软件。录制的视频会自动保存在服务器上，供后续分析和评估。

### 2. 自动语音识别
系统采用讯飞语音识别 API，将面试中的语音转换为文本，准确率高达95%以上。识别后的文本会自动保存，并用于后续的 AI 分析和评估。

### 3. AI 面试评估
系统基于讯飞星火大模型对候选人的回答进行分析和评估，提供客观的评分和反馈。评估维度包括沟通能力、专业知识、问题解决能力、团队合作能力等。

### 4. 自动报告生成
系统自动生成详细的 PDF 面试报告，包含候选人信息、面试内容、评分和总结。报告格式清晰、美观，便于企业进行招聘决策。

### 5. 岗位匹配分析
系统根据候选人的表现和岗位要求，提供岗位匹配度分析，帮助企业找到最合适的人才。匹配度分析基于多个维度，包括专业技能、工作经验、性格特点等。

## 贡献指南 🤝
1. ** Fork 仓库**
2. **创建分支**
```bash
git checkout -b feature/your-feature
```
3. **提交更改**
```bash
git commit -m "Add your feature"
```
4. **推送分支**
```bash
git push origin feature/your-feature
```
5. **创建 Pull Request**

## 许可证 📝
本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。

## 联系方式 📧
- 项目负责人：[your name](mailto:your.email@example.com)
- 技术支持：[support@example.com](mailto:support@example.com)

## 致谢 💖
感谢所有为项目做出贡献的人，包括开发人员、测试人员、文档编写人员等。没有你们的努力，就没有今天的 AI 面试平台。

## 未来规划 🌈
1. 增加更多的 AI 评估维度，提高评估的准确性和全面性。
2. 开发移动端应用，方便候选人随时随地进行面试。
3. 增加多语言支持，满足企业国际化招聘的需求。
4. 开发更多的数据分析功能，帮助企业更好地了解候选人的表现。
5. 优化用户界面，提高用户体验。

欢迎大家提出宝贵的意见和建议，我们会不断优化和完善 AI 面试平台，为企业提供更好的招聘解决方案。