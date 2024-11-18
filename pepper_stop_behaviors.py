# coding=utf-8

from naoqi import ALProxy

# 设定Pepper机器人的IP地址和端口号
IP = "169.254.219.214"
PORT = 9559

def stop_all_behaviors(ip, port):
    try:
        # 创建行为管理代理
        motion_proxy = ALProxy("ALBehaviorManager", ip, port)
        
        # 检查是否有正在运行的行为
        if motion_proxy.getRunningBehaviors():
            # 停止所有正在运行的行为
            motion_proxy.stopAllBehaviors()
            print("已停止所有正在运行的行为。")
        else:
            print("当前没有正在运行的行为。")
    except Exception as e:
        print("停止行为时出现错误: " + str(e))

if __name__ == "__main__":
    stop_all_behaviors(IP, PORT)
