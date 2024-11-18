# coding: utf-8
# 合并后的 Python 2 代码：Pepper 机器人执行等待类动作并等待唤醒词

import requests
import json
import time
import speech_recognition as sr
import threading
import random
from naoqi import ALProxy
from collections import deque

# 服务器地址
url = "http://127.0.0.1:5000/chat"  # 本地运行时使用 localhost，指向 /chat 端点以调用大模型

# Pepper 机器人的 IP 地址和端口
PEPPER_IP = "169.254.219.214"  # 请替换为您的 Pepper IP
PEPPER_PORT = 9559

# 初始化代理
tts = None
animated_speech = None
touch_proxy = None
motion_proxy = None

try:
    tts = ALProxy("ALTextToSpeech", PEPPER_IP, PEPPER_PORT)
    animated_speech = ALProxy("ALAnimatedSpeech", PEPPER_IP, PEPPER_PORT)
    touch_proxy = ALProxy("ALTouch", PEPPER_IP, PEPPER_PORT)
    motion_proxy = ALProxy("ALBehaviorManager", PEPPER_IP, PEPPER_PORT)
except Exception as e:
    print("无法连接到 Pepper 的模块: " + str(e))

# 定义等待类动作列表
waiting_animations = [
    "animations/Stand/Waiting/AirGuitar_1",
    "animations/Stand/Waiting/BreathLoop_1",
    "animations/Stand/Waiting/BreathLoop_2",
    "animations/Stand/Waiting/BreathLoop_3",
    "animations/Stand/Waiting/DriveCar_1",
    "animations/Stand/Waiting/Helicopter_1",
    "animations/Stand/Waiting/HideEyes_1",
    "animations/Stand/Waiting/HideHands_1",
    "animations/Stand/Waiting/LookHand_1",
    "animations/Stand/Waiting/LookHand_2",
    "animations/Stand/Waiting/LoveYou_1",
    "animations/Stand/Waiting/Monster_1",
    "animations/Stand/Waiting/PlayHands_1",
    "animations/Stand/Waiting/PlayHands_2",
    "animations/Stand/Waiting/PlayHands_3",
    "animations/Stand/Waiting/Relaxation_1",
    "animations/Stand/Waiting/Relaxation_2",
    "animations/Stand/Waiting/Relaxation_3",
    "animations/Stand/Waiting/Relaxation_4",
    "animations/Stand/Waiting/Rest_1",
    "animations/Stand/Waiting/Robot_1",
    "animations/Stand/Waiting/ScratchBack_1",
    "animations/Stand/Waiting/ScratchBottom_1",
    "animations/Stand/Waiting/ScratchEye_1",
    "animations/Stand/Waiting/ScratchHand_1",
    "animations/Stand/Waiting/ScratchHead_1",
    "animations/Stand/Waiting/ScratchLeg_1",
    "animations/Stand/Waiting/ScratchTorso_1",
    "animations/Stand/Waiting/ShowMuscles_1",
    "animations/Stand/Waiting/ShowMuscles_2",
    "animations/Stand/Waiting/ShowMuscles_3",
    "animations/Stand/Waiting/ShowMuscles_4",
    "animations/Stand/Waiting/ShowMuscles_5",
    "animations/Stand/Waiting/Think_1",
    "animations/Stand/Waiting/Think_2",
    "animations/Stand/Waiting/Think_3",
    "animations/Stand/Waiting/Think_4",
    "animations/Stand/Waiting/Waddle_1",
    "animations/Stand/Waiting/Waddle_2",
    "animations/Stand/Waiting/WakeUp_1",
    "animations/Stand/Waiting/Zombie_1"
]

# 定义反应类动作列表
reaction_animations = [
    "animations/Stand/Reactions/ShakeBody_1",
    "animations/Stand/Reactions/ShakeBody_2",
    "animations/Stand/Reactions/ShakeBody_3",
    "animations/Stand/Reactions/TouchHead_1",
    "animations/Stand/Reactions/TouchHead_2",
    "animations/Stand/Reactions/TouchHead_3",
    "animations/Stand/Reactions/TouchHead_4",
    "animations/Stand/Reactions/SeeSomething_1",
    "animations/Stand/Reactions/SeeSomething_3",
    "animations/Stand/Reactions/SeeSomething_4",
    "animations/Stand/Reactions/SeeSomething_5",
    "animations/Stand/Reactions/SeeSomething_6",
    "animations/Stand/Reactions/SeeSomething_7",
    "animations/Stand/Reactions/SeeSomething_8"
]

# 使用双端队列来记录最近执行的动作，避免短时间内重复
recent_animations = deque(maxlen=5)

# 全局变量
waiting_mode = True  # 标志当前是否处于等待唤醒词的模式
stop_event = threading.Event()  # 用于线程的停止控制

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

# 触摸检测函数
def detect_touch(ip, port):
    global waiting_mode, stop_event
    try:
        touch_proxy = ALProxy("ALTouch", ip, port)
        motion_proxy = ALProxy("ALBehaviorManager", ip, port)
        while not stop_event.is_set():
            # 检查是否处于等待模式
            # 如果需要在任何模式下都检测触摸，可以注释掉下面两行
            if not waiting_mode:
                time.sleep(1)
                continue
            # 检测触摸事件
            touch_events = touch_proxy.getStatus()
            if any(event[1] for event in touch_events):
                for sensor in touch_events:
                    if sensor[1]:  # 如果传感器被触摸
                        print("检测到触摸: 传感器名称: {}, 传感器ID: {}".format(sensor[0], sensor[2]))
                        # 停止所有行为
                        motion_proxy.stopAllBehaviors()
                        print("已停止所有行为。")
                        # 随机选择一个反应类动作
                        random_reaction = random.choice(reaction_animations)
                        if motion_proxy.isBehaviorInstalled(random_reaction):
                            motion_proxy.runBehavior(random_reaction)
                            print("执行反应动作: {}".format(random_reaction))
                        else:
                            print("行为未安装: {}".format(random_reaction))
                        time.sleep(1)  # 等待一段时间以防止重复触发
            time.sleep(0.5)  # 防止 CPU 过载
    except Exception as e:
        print("检测触摸失败: " + str(e))

# 执行等待类动作
def perform_random_waiting_animation(ip, port):
    global waiting_mode, stop_event, recent_animations
    try:
        motion_proxy = ALProxy("ALBehaviorManager", ip, port)
        while not stop_event.is_set():
            if not waiting_mode:
                time.sleep(1)
                continue
            # 随机选择一个等待类动作，避免近期重复
            random_animation = random.choice([anim for anim in waiting_animations if anim not in recent_animations])
            if motion_proxy.isBehaviorInstalled(random_animation):
                # 异步运行行为
                behavior_id = motion_proxy.post.runBehavior(random_animation)
                print("执行等待动作: {}".format(random_animation))
                recent_animations.append(random_animation)
                # 检查等待模式状态，如果变为 False，则停止当前行为
                while motion_proxy.isBehaviorRunning(random_animation):
                    if not waiting_mode:
                        motion_proxy.stopBehavior(random_animation)
                        print("停止等待动作: {}".format(random_animation))
                        break
                    time.sleep(0.1)
            else:
                print("行为未安装: {}".format(random_animation))
            # 休眠一小段时间
            time.sleep(random.uniform(0.5, 1.0))
    except Exception as e:
        print("执行等待动作失败: " + str(e))

# 启动唤醒词识别以启动聊天功能
def trigger_recognition_on_keyword(ip, port):
    global waiting_mode, stop_event
    try:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        recognizer.dynamic_energy_threshold = False  # 禁用动态能量阀值以提高响应速度
        recognizer.energy_threshold = 300  # 手动设置较低的能量阀值以提高效果

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

        waiting_mode = True  # 设置等待模式为 True

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
                        waiting_mode = False  # 检测到唤醒词，设置等待模式为 False
                        motion_proxy.stopAllBehaviors()  # 停止所有当前行为
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
    global waiting_mode, stop_event
    try:
        waiting_mode = False  # 确保等待模式为 False
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
            animated_speech.say("^start(" + chosen_behavior + ") Ready to chat! Just say 'Goodbye' if you want me to take a break.")
        print("Speech recognition started.")

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
                    if "Goodbye" in recognized_text.lower():
                        waiting_mode = True  # 设置等待模式为 True
                        motion_proxy.stopAllBehaviors()  # 停止所有当前行为
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
        # 启动触摸检测线程
        touch_thread = threading.Thread(target=detect_touch, args=(PEPPER_IP, PEPPER_PORT))
        touch_thread.start()
        # 启动等待类动作线程
        waiting_animation_thread = threading.Thread(target=perform_random_waiting_animation, args=(PEPPER_IP, PEPPER_PORT))
        waiting_animation_thread.start()
        try:
            trigger_recognition_on_keyword(PEPPER_IP, PEPPER_PORT)
        except KeyboardInterrupt:
            print("程序已终止。")
    else:
        print("Connection test failed.")

    # 停止所有线程
    stop_event.set()
    touch_thread.join()
    waiting_animation_thread.join()
    print("程序已结束。")
