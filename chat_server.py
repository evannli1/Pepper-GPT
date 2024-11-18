# Python 3 环境代码: Flask 服务器
from flask import Flask, request, jsonify
import groq
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化 Groq 客户端
client = groq.Groq(api_key=os.getenv('GROQ_API_KEY'))

# 初始化 Flask 应用
app = Flask(__name__)

# 读取系统消息的内容
with open('assistant_instructions.txt', 'r', encoding='utf-8') as file:
    system_message_content = file.read().strip()

# 初始化一个空的消息列表，用于存储对话历史
messages = [
    {
        "role": "system",
        "content": system_message_content
    }
]

@app.route('/chat', methods=['POST'])
def chat():
    global messages
    # 从请求中获取消息数据
    data = request.json
    user_message = data['messages'][0]

    # 将用户输入添加到消息列表中
    messages.append(user_message)

    # 使用 Groq API 获取模型回复
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="mixtral-8x7b-32768",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )

    # 获取模型的回复内容
    assistant_message = {
        "role": "assistant",
        "content": chat_completion.choices[0].message.content
    }
    messages.append(assistant_message)

    response = {
        "content": assistant_message['content']
    }
    return jsonify(response)

@app.route('/echo', methods=['POST'])
def echo():
    # 从请求中获取消息数据
    data = request.json
    user_message = data['message']

    # 返回相同的消息内容
    response = {
        "content": user_message
    }
    return jsonify(response)

if __name__ == '__main__':
    # 启动 Flask 服务器，监听 0.0.0.0 主机地址和 5000 端口，以便本地和其他设备访问
    app.run(host='0.0.0.0', port=5000, debug=True)
