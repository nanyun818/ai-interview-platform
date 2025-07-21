with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()
    # 搜索与职位相关的关键词
    keywords = ['fetch("http://localhost:5000/chat"', 'method: "POST"', 'body: JSON.stringify', 'message: message', 'position: ']
    for keyword in keywords:
        if keyword in content:
            # 打印匹配关键词前后的上下文
            index = content.find(keyword)
            start = max(0, index - 100)
            end = min(len(content), index + 100)
            print(f'=== 找到关键词: {keyword} ===')
            print(content[start:end])
            print('\n')