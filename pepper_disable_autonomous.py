# coding=utf-8

from naoqi import ALProxy

# 设定Pepper机器人的IP地址和端口号
IP = "169.254.219.214"
PORT = 9559

def disable_autonomous_life(ip, port):
    try:
        # 创建自主生命代理
        life_proxy = ALProxy("ALAutonomousLife", ip, port)

        # 检查当前自主生命模式
        current_state = life_proxy.getState()
        print("当前自主生命模式: {}".format(current_state))

        # 如果自主生命已启动，关闭自主生命
        if current_state != "disabled":
            print("正在关闭自主生命...")
            life_proxy.setState("disabled")
            print("自主生命已关闭。")
        else:
            print("自主生命已经是关闭状态。")

    except Exception as e:
        print("关闭自主生命失败: " + str(e))

if __name__ == "__main__":
    disable_autonomous_life(IP, PORT)
