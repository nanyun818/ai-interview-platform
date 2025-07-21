import os
from app import app

# 启动Flask应用
if __name__ == '__main__':
    port = 5000
    print(f'Flask服务器启动在 http://localhost:{port}')
    app.run(host='0.0.0.0', port=port, debug=True)