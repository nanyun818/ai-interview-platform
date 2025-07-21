import os
from app import app

# 打印API密钥配置
print("APPID:", os.environ.get('XINGHUO_APPID', '73c06b9a'))
print("API_KEY:", os.environ.get('XINGHUO_API_KEY', '6304d19fe686af9213246de50161e0da'))
print("API_SECRET:", os.environ.get('XINGHUO_API_SECRET', 'ODEXNTk4ZmRlMWJjM2FiYmU2NGNhNGEw'))

print("测试完成。如果上面显示了正确的API密钥配置，则说明更新成功。")