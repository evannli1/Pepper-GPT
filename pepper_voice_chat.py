# coding: utf-8
# Python 2 环境代码：合并 Flask 服务器通讯和语音识别控制
import requests
import json
import time
import speech_recognition as sr
import threading
import random
from naoqi import ALProxy

# 服务器地址
url = "http://127.0.0.1:5000/chat"  # 本地运行时使用 localhost，指向 /chat 端点以调用大模型

# Pepper 机器人的 IP 地址和端口
PEPPER_IP = "169.254.219.214"
PEPPER_PORT = 9559

# 初始化文本到语音的代理和动画语音代理
tts = None
animated_speech = None
try:
    tts = ALProxy("ALTextToSpeech", PEPPER_IP, PEPPER_PORT)
    animated_speech = ALProxy("ALAnimatedSpeech", PEPPER_IP, PEPPER_PORT)
except Exception as e:
    print("无法连接到 Pepper 的模块: " + str(e))

# 测试与 Pepper 的连接
def test_connection(ip, port):
    try:
        tts_test = ALProxy("ALTextToSpeech", ip, port)
        # 随机选择一个行为
        behaviors = [
            "animations/Stand/Emotions/Positive/Happy_1",
            "animations/Stand/Emotions/Positive/Happy_2",
            "animations/Stand/Emotions/Positive/Happy_3",
            "animations/Stand/Emotions/Positive/Happy_4",
            "animations/Stand/Emotions/Positive/Proud_1",
            "animations/Stand/Emotions/Positive/Proud_2",
            "animations/Stand/Emotions/Positive/Winner_1",
            "animations/Stand/BodyTalk/Speaking/BodyTalk_8"
        ]
        chosen_behavior = random.choice(behaviors)
        animated_speech.say("^start(" + chosen_behavior + ") Woohoo! Hey there, it's Pepper here! Looks like we're all set to roll!")
        
        version_proxy = ALProxy("ALSystem", ip, port)
        robot_version = version_proxy.systemVersion()
        print("Connected to Pepper. System version: " + robot_version)
        return True
    except Exception as e:
        print("Connection failed: " + str(e))
        return False

# 启动指令 ALAnimatedSpeech 进行语音转换
def speak_with_animation(animated_speech, text):
    try:
        # 随机选择一个行为
        behaviors = [
            "animations/Stand/BodyTalk/Speaking/BodyTalk_1",
            "animations/Stand/BodyTalk/Speaking/BodyTalk_2",
            "animations/Stand/BodyTalk/Speaking/BodyTalk_3",
            "animations/Stand/BodyTalk/Speaking/BodyTalk_4",
            "animations/Stand/Emotions/Positive/Happy_2",
            "animations/Stand/Gestures/Explain_3"
        ]
        chosen_behavior = random.choice(behaviors)
        animated_speech.say("^start(" + chosen_behavior + ") " + text)
    except Exception as e:
        print("Error during animated speech: " + str(e))

# 启动唤醒词识别以启动聊天功能
def trigger_recognition_on_keyword(ip, port):
    try:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        recognizer.dynamic_energy_threshold = False  # 禁用动态能量队值以提高响应速度
        recognizer.energy_threshold = 300  # 手动设置较低的能量队值以提高效果

        # 启动唤醒词识别
        if animated_speech:
            # 随机选择一个行为
            behaviors = [
                "animations/Stand/Emotions/Neutral/AskForAttention_1",
                "animations/Stand/Emotions/Neutral/AskForAttention_2",
                "animations/Stand/Emotions/Neutral/AskForAttention_3",
                "animations/Stand/Emotions/Neutral/Cautious_1",
                "animations/Stand/Emotions/Neutral/Suspicious_1",
                "animations/Stand/BodyTalk/Listening/Listening_3",
                "animations/Stand/BodyTalk/Listening/Listening_7"
            ]
            chosen_behavior = random.choice(behaviors)
            animated_speech.say("^start(" + chosen_behavior + ") Hehe, just say 'hi' or 'hello', and I'll wake up, okay?")
        print("Waiting for wake-up word 'hi' or 'hello'.")

        # 保持程序运行，直到检测到唤醒词
        while True:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.1)  # 缩短环境噪声调整时间以提高响应速度
                print("Listening for wake-up word...")
                try:
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)  # 取消整体超时，提高效果
                    recognized_text = recognizer.recognize_google(audio)
                    print("Recognized: " + recognized_text)
                    if "hi" in recognized_text.lower() or "hello" in recognized_text.lower():
                        if animated_speech:
                            # 随机选择一个行为
                            behaviors = [
                                "animations/Stand/BodyTalk/Listening/Listening_1",
                                "animations/Stand/BodyTalk/Listening/Listening_2",
                                "animations/Stand/BodyTalk/Listening/Listening_4",
                                "animations/Stand/BodyTalk/Listening/Listening_6",
                                "animations/Stand/BodyTalk/Listening/Listening_7",
                                "animations/Stand/Emotions/Positive/Interested_1",
                                "animations/Stand/Emotions/Positive/Interested_2"
                            ]
                            chosen_behavior = random.choice(behaviors)
                            animated_speech.say("^start(" + chosen_behavior + ") Oh, you got my attention! Go ahead, I’m all ears!")
                        start_continuous_recognition(ip, port)
                        break
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio.")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                    if animated_speech:
                        animated_speech.say("Uh-oh, looks like I can't reach the speech recognition service right now.")
                except Exception as e:
                    print("Unexpected error during wake-up recognition: " + str(e))
                    continue

    except Exception as e:
        print("Wake-up recognition failed: " + str(e))

# 启动语音识别和交互过程时使用此方法来发起 ALAnimatedSpeech
def start_continuous_recognition(ip, port):
    try:
        if animated_speech:
            # 随机选择一个行为
            behaviors = [
                "animations/Stand/BodyTalk/Listening/Listening_3",
                "animations/Stand/BodyTalk/Speaking/BodyTalk_5",
                "animations/Stand/BodyTalk/Speaking/BodyTalk_9",
                "animations/Stand/BodyTalk/Speaking/BodyTalk_11",
                "animations/Stand/BodyTalk/Speaking/BodyTalk_14"
            ]
            chosen_behavior = random.choice(behaviors)
            animated_speech.say("^start(" + chosen_behavior + ") Ready to chat! Just say 'stop listening' if you want me to take a break.")
        print("Speech recognition started.")

        # 定义一个停止标志  
        stop_event = threading.Event()
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        recognizer.dynamic_energy_threshold = False  # 禁用动态能量阀值以提高响应速度
        recognizer.energy_threshold = 300  # 手动设置较低的能量阀值以提高效果

        while not stop_event.is_set():
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.1)  # 缩短环境噪声调整时间以提高响应速度
                print("Listening for user input...")
                try:
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)  # 取消整体超时，提高效果
                    recognized_text = recognizer.recognize_google(audio)
                    print("Recognized: " + recognized_text)
                    
                    # 如果检测到“stop listening”命令，退出持续检测并重新进入待唤醒状态
                    if "stop listening" in recognized_text.lower():
                        if animated_speech:
                            # 随机选择一个行为
                            behaviors = [
                                "animations/Stand/Emotions/Positive/Peaceful_1",
                                "animations/Stand/Emotions/Neutral/CalmDown_1",
                                "animations/Stand/Emotions/Neutral/CalmDown_2",
                                "animations/Stand/Emotions/Positive/Relieved_1",
                                "animations/Stand/Emotions/Neutral/Relaxation_1",
                                "animations/Stand/Emotions/Positive/Sure_1"
                            ]
                            chosen_behavior = random.choice(behaviors)
                            animated_speech.say("^start(" + chosen_behavior + ") Got it, I’ll go into stealth mode now. But hey, don’t forget me, okay?")
                        print("Entering wake-up mode.")
                        trigger_recognition_on_keyword(ip, port)
                        return

                    # 准备请求数据，发送到服务器进行聊天
                    data = {"messages": [
                        {"role": "user", "content": recognized_text}
                    ]}
                    headers = {"Content-Type": "application/json"}

                    # 发送 POST 请求到服务器
                    response = requests.post(url, data=json.dumps(data), headers=headers)

                    # 处理返回结果
                    if response.status_code == 200:
                        server_response = response.json()["content"]  # 保持为 Unicode 格式
                        print(u"服务器返回: {}".format(server_response))  # 打印 Unicode 响应
                        
                        # 使用 ALAnimatedSpeech 进行输出，并随机选择行为
                        if animated_speech:
                            speak_with_animation(animated_speech, server_response.encode('utf-8'))
                    else:
                        print("Error:", response.status_code, response.text)
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio.")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                    if animated_speech:
                        # 随机选择一个行为
                        behaviors = [
                            "animations/Stand/Emotions/Negative/Sorry_1",
                            "animations/Stand/Emotions/Negative/Sad_1",
                            "animations/Stand/Emotions/Negative/Disappointed_1",
                            "animations/Stand/Emotions/Negative/Hurt_1",
                            "animations/Stand/Emotions/Negative/Hurt_2",
                            "animations/Stand/Emotions/Neutral/Embarrassed_1",
                            "animations/Stand/Emotions/Negative/Exhausted_1"
                        ]
                        chosen_behavior = random.choice(behaviors)
                        animated_speech.say("^start(" + chosen_behavior + ") Uh-oh, looks like I can't reach the speech recognition service right now.")
                except sr.WaitTimeoutError:
                    print("Listening timed out while waiting for phrase to start. Continuing to listen...")
                    continue
                except Exception as e:
                    print("Unexpected error during continuous recognition: " + str(e))
                    continue
    except Exception as e:
        print("Speech recognition and communication failed: " + str(e))

# 主程序入口
if __name__ == "__main__":
    if test_connection(PEPPER_IP, PEPPER_PORT):
        print("Connection test passed.")
        trigger_recognition_on_keyword(PEPPER_IP, PEPPER_PORT)
    else:
        print("Connection test failed.")
