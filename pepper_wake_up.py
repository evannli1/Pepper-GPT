# coding=utf-8

from naoqi import ALProxy
import time

# 设定Pepper机器人的IP地址和端口号
IP = "169.254.219.214"
PORT = 9559

def wake_up_pepper_and_prevent_sleep(ip, port):
    try:
        # 创建运动控制代理
        motion_proxy = ALProxy("ALMotion", ip, port)
        
        # 唤醒Pepper机器人
        motion_proxy.wakeUp()
        print("Pepper已唤醒。")
        
        # 设置所有电机的刚度为 1.0，以防止进入休眠状态
        body_names = motion_proxy.getBodyNames("Body")
        motion_proxy.setStiffnesses(body_names, 1.0)
        print("Pepper的电机已设置为刚度模式，不会进入休眠状态。")
        
    except Exception as e:
        print("唤醒Pepper或防止休眠失败: " + str(e))

if __name__ == "__main__":
    wake_up_pepper_and_prevent_sleep(IP, PORT)
