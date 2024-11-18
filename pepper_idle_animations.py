# coding=utf-8

from naoqi import ALProxy
import random
import time
from threading import Thread
from collections import deque

# 设定Pepper机器人的IP地址和端口号
IP = "169.254.219.214"
PORT = 9559

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

stop_flag = False

def stop_all_behaviors(ip, port):
    try:
        # 创建行为代理
        motion_proxy = ALProxy("ALBehaviorManager", ip, port)
        # 停止所有当前正在运行的行为
        motion_proxy.stopAllBehaviors()
        print("已停止所有当前运行的行为。")
    except Exception as e:
        print("停止当前行为失败: " + str(e))

def start_basic_awareness(ip, port):
    try:
        # 创建基本感知代理
        awareness_proxy = ALProxy("ALBasicAwareness", ip, port)
        
        # 开启基本感知功能
        awareness_proxy.startAwareness()
        print("基本感知功能已开启。")
    except Exception as e:
        print("开启基本感知功能失败: " + str(e))

def detect_touch(ip, port):
    global stop_flag
    try:
        # 创建行为代理
        motion_proxy = ALProxy("ALBehaviorManager", ip, port)
        touch_proxy = ALProxy("ALTouch", ip, port)
        while True:
            if stop_flag:
                break
            # 检测是否有触摸事件
            touch_events = touch_proxy.getStatus()
            if any(event[1] for event in touch_events):
                for sensor in touch_events:
                    if sensor[1]:  # 如果传感器被触摸
                        print("检测到触摸: 传感器名称: {}, 传感器ID: {}".format(sensor[0], sensor[2]))
                        # 停止当前行为
                        motion_proxy.stopAllBehaviors()
                        print("已停止当前行为。")
                        # 随机选择一个反应类动作
                        random_reaction = random.choice(reaction_animations)
                        if motion_proxy.isBehaviorInstalled(random_reaction):
                            motion_proxy.runBehavior(random_reaction)
                            print("执行反应动作: {}".format(random_reaction))
                        else:
                            print("行为未安装: {}".format(random_reaction))
                        time.sleep(1)  # 适当等待以防止重复触发
                        # 执行完反应动作后返回等待类动作
                        perform_random_waiting_animation(ip, port)
    except Exception as e:
        print("检测触摸失败: " + str(e))

def perform_random_waiting_animation(ip, port):
    global stop_flag
    try:
        # 创建行为代理
        motion_proxy = ALProxy("ALBehaviorManager", ip, port)
        
        # 循环执行随机等待类动作
        while True:
            if stop_flag:
                break
            
            # 停止所有当前正在运行的行为，确保后续动作不冲突
            motion_proxy.stopAllBehaviors()
            print("停止所有当前行为以准备执行新的动作。")
            
            # 随机选择一个等待类动作，确保不会短时间内重复
            random_animation = random.choice([anim for anim in waiting_animations if anim not in recent_animations])
            
            # 如果行为存在则启动该行为
            if motion_proxy.isBehaviorInstalled(random_animation):
                motion_proxy.runBehavior(random_animation)
                print("执行等待动作: {}".format(random_animation))
                recent_animations.append(random_animation)  # 记录已执行的动作
            else:
                print("行为未安装: {}".format(random_animation))
            
            # 休眠一小段时间，使动作衔接更加流畅，模拟自然的连贯性
            time.sleep(random.uniform(0.5, 1.0))
    except Exception as e:
        print("执行等待动作失败: " + str(e))

if __name__ == "__main__":
    stop_all_behaviors(IP, PORT)
    start_basic_awareness(IP, PORT)
    
    # 创建并启动触摸检测线程
    touch_thread = Thread(target=detect_touch, args=(IP, PORT))
    touch_thread.start()
    
    try:
        # 执行等待类动作
        perform_random_waiting_animation(IP, PORT)
    except KeyboardInterrupt:
        stop_flag = True
        touch_thread.join()
        print("程序已终止。")