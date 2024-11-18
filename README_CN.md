# Pepper-GPT 控制器

这是一个用于控制Pepper机器人的Python项目，集成了GPT对话功能，实现了语音交互、人脸追踪、动作控制等功能。

[English Documentation](README.md)

## 功能特点

- 人脸检测和追踪
- 语音识别和对话
- 自动等待动作
- 触摸响应
- GPT对话集成
- 基础感知控制

## 文件结构

- `pepper_face_tracking.py`: 人脸检测和追踪功能
- `pepper_idle_animations.py`: 等待动作和触摸响应
- `pepper_basic_awareness.py`: 基础感知功能
- `pepper_disable_autonomous.py`: 自主生命控制
- `pepper_stop_behaviors.py`: 行为控制
- `pepper_wake_up.py`: 唤醒功能
- `pepper_voice_chat.py`: 语音对话功能
- `pepper_main_controller.py`: 主控制程序
- `chat_server.py`: GPT对话服务器

## 环境要求

### 软件要求
- Python 2.7（用于Pepper机器人控制）
- Python 3.x（用于GPT服务器）
- NAOqi SDK 2.5.5+
- OpenCV 4.5.0+
- 其他依赖见requirements.txt

### 硬件要求
- Pepper机器人
- 带网络连接的电脑
- 麦克风（用于语音识别）

### NAOqi SDK 安装
1. 从Softbank Robotics网站下载NAOqi SDK
2. 将SDK解压到指定位置
3. 设置环境变量：
```bash
export PYTHONPATH=${PYTHONPATH}:/path/to/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/path/to/pynaoqi-python2.7-2.5.5.5-linux64/lib
```

## 安装步骤

1. 克隆仓库：
```bash
git clone [repository-url]
cd Pepper-GPT
```

2. 创建并激活Python 2.7虚拟环境（用于Pepper控制）：
```bash
virtualenv -p python2.7 venv_pepper
source venv_pepper/bin/activate
pip install -r requirements_pepper.txt
```

3. 创建并激活Python 3.x虚拟环境（用于GPT服务器）：
```bash
python3 -m venv venv_server
source venv_server/bin/activate
pip install -r requirements.txt
```

4. 配置环境：
```bash
cp .env.example .env
```
编辑`.env`文件，填入：
- Groq API密钥
- Pepper机器人IP地址
- Pepper机器人端口

## 使用说明

1. 启动GPT服务器（在Python 3.x环境中）：
```bash
source venv_server/bin/activate
python3 chat_server.py
```

2. 在新终端中运行主控制程序（在Python 2.7环境中）：
```bash
source venv_pepper/bin/activate
python2 pepper_main_controller.py
```

## 功能详解

### 人脸追踪
- 使用OpenCV进行实时人脸检测
- 自动头部运动跟随检测到的人脸
- 嘴部检测和响应

### 语音交互
- 唤醒词检测（"hi"或"hello"）
- 持续语音识别
- 使用GPT进行自然语言处理
- 带动画的语音回应

### 等待行为
- 多种预定义动画
- 触摸传感器响应
- 自动行为切换
- 自然运动模式

### 系统控制
- 自主生命管理
- 基础感知控制
- 行为管理
- 唤醒和休息状态

## 故障排除

### 常见问题
1. NAOqi连接错误
   - 检查Pepper是否在同一网络中
   - 验证IP地址和端口
   - 确保NAOqi SDK正确安装

2. 语音识别问题
   - 检查麦克风连接
   - 验证网络连接
   - 根据需要调整噪声阈值

3. GPT服务器问题
   - 验证.env文件中的API密钥
   - 检查服务器日志
   - 确保Python 3.x环境处于激活状态

## 参与贡献

1. Fork本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

[选择合适的许可证]

## 作者

[你的名字]

## 致谢

- 感谢SoftBank Robotics提供Pepper机器人和NAOqi SDK
- 感谢Groq提供GPT API
- 感谢OpenCV社区
