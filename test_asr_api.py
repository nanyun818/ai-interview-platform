import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入app.py中的函数
from app import generate_ai_summary

# 测试函数
if __name__ == '__main__':
    print("测试讯飞星火API密钥配置...")
    
    # 调用函数来测试API密钥配置
    try:
        # 传递一个简单的prompt来测试
        result = generate_ai_summary("测试")
        print(f"函数调用结果类型: {type(result)}")
        print(f"函数调用结果: {result}")
        print("API密钥配置成功!")
    except Exception as e:
        print(f"函数调用失败: {e}")
        print(f"错误类型: {type(e)}")
        import traceback
        traceback.print_exc()
        print("API密钥配置失败!")