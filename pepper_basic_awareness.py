# coding=utf-8

from naoqi import ALProxy

# 设定Pepper机器人的IP地址和端口号
IP = "169.254.219.214"
PORT = 9559

def start_basic_awareness(ip, port):
    try:
        # 创建基本感知代理
        awareness_proxy = ALProxy("ALBasicAwareness", ip, port)
        
        # 开启基本感知功能
        awareness_proxy.startAwareness()
        print("基本感知功能已开启。")
    except Exception as e:
        print("开启基本感知功能失败: " + str(e))

if __name__ == "__main__":
    start_basic_awareness(IP, PORT)
