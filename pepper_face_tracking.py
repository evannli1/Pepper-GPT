# coding=utf-8

import sys
import time
import random
import cv2
import numpy as np
import threading
from naoqi import ALProxy

# 设定Pepper机器人的IP地址和端口号
IP = "169.254.219.214"
PORT = 9559

def test_connection(ip, port):
    try:
        tts = ALProxy("ALTextToSpeech", ip, port)
        version_proxy = ALProxy("ALSystem", ip, port)
        robot_version = version_proxy.systemVersion()
        print("Connected to Pepper. System version: " + robot_version)
        
        return True
    except Exception as e:
        print("Connection failed: " + str(e))
        return False

def display_camera_feed(ip, port, video_client):
    video_proxy = ALProxy("ALVideoDevice", ip, port)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    mouth_cascade_path = cv2.data.haarcascades + 'haarcascade_mcs_mouth.xml'
    
    # 检查嘴巴检测分类器文件是否存在
    if not mouth_cascade_path or not cv2.CascadeClassifier(mouth_cascade_path).load(mouth_cascade_path):
        print("Warning: Mouth cascade file not found or failed to load. Mouth detection will be disabled.")
        mouth_cascade = None
    else:
        mouth_cascade = cv2.CascadeClassifier(mouth_cascade_path)
    
    while True:
        frame = video_proxy.getImageRemote(video_client)
        if frame is not None:
            width = frame[0]
            height = frame[1]
            array = frame[6]
            image = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))
            
            # 转换为灰度图像用于检测
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 检测人脸
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = image[y:y+h, x:x+w]
                
                # 检测嘴巴位置（如果嘴巴分类器可用）
                if mouth_cascade is not None:
                    mouths = mouth_cascade.detectMultiScale(roi_gray, 1.5, 11)
                    for (mx, my, mw, mh) in mouths:
                        # 只检测最接近下部的嘴巴
                        if my > h / 2:
                            cv2.rectangle(roi_color, (mx, my), (mx+mw, my+mh), (0, 255, 0), 2)
                            # 如果检测到嘴巴，抬头寻找眼睛
                            motion_proxy = ALProxy("ALMotion", ip, port)
                            motion_proxy.setAngles("HeadPitch", -0.1, 0.1)  # 抬头
                            break
            
            # 显示摄像头画面
            cv2.imshow("Pepper Camera", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    # 关闭摄像头画面窗口
    cv2.destroyAllWindows()
    video_proxy.unsubscribe(video_client)

def face_recognition(ip, port):
    try:
        motion_proxy = ALProxy("ALMotion", ip, port)
        face_proxy = ALProxy("ALFaceDetection", ip, port)
        memory_proxy = ALProxy("ALMemory", ip, port)
        tracker = ALProxy("ALTracker", ip, port)
        video_proxy = ALProxy("ALVideoDevice", ip, port)
        
        # 注册视频流
        resolution = 2  # 640x480
        color_space = 13  # BGR颜色空间
        fps = 15
        video_client = video_proxy.subscribe("python_client", resolution, color_space, fps)
        
        # 启动摄像头画面显示的线程
        camera_thread = threading.Thread(target=display_camera_feed, args=(ip, port, video_client))
        camera_thread.start()
        
        # 抬头至正常高度
        motion_proxy.setStiffnesses("Head", 1.0)
        motion_proxy.setAngles("HeadPitch", -0.4, 0.1)  # 明显抬头
        
        # 启动人脸识别
        face_proxy.subscribe("Face")
        print("Starting face recognition. Pepper is scanning...")
        
        # 注册人脸目标并开始跟踪
        tracker.registerTarget("Face", 0.1)
        tracker.setEffector("None")  # 使用头部进行跟踪

        # 增加自主行为，模拟机器人像在探索周围环境
        exploration_mode = True

        while True:
            face_data = memory_proxy.getData("FaceDetected")
            
            if face_data:
                exploration_mode = False
                print("Face detected. Tracking...")
                
                tracker.track("Face")  # 持续跟踪人脸
            else:
                if not exploration_mode:
                    exploration_mode = True
                
                print("Lost the face, scanning...")
                tracker.stopTracker()  # 停止当前跟踪
                
                # 自主探索模式，机器人会表现出好奇心，四处张望
                for _ in range(3):  # 随机扫描几次
                    yaw_angle = random.uniform(-0.8, 0.8)  # 水平左右随机
                    pitch_angle = -0.4  # 抬头和低头随机
                    
                    motion_proxy.setAngles("HeadYaw", yaw_angle, 0.1)
                    motion_proxy.setAngles("HeadPitch", pitch_angle, 0.1)
                    time.sleep(0.5)  # 减少等待时间以加快扫描速度
                    face_data = memory_proxy.getData("FaceDetected")
                    
                    if face_data:
                        print("Face reacquired.")
                        tracker.track("Face")
                        exploration_mode = False
                        break
        
        # 取消所有订阅和跟踪
        tracker.stopTracker()
        tracker.unregisterAllTargets()
        face_proxy.unsubscribe("Face")
        
        # 恢复头部位置
        motion_proxy.setAngles("HeadYaw", 0.0, 0.1)
        motion_proxy.setAngles("HeadPitch", 0.0, 0.1)
    except Exception as e:
        print("Face recognition failed: " + str(e))

if __name__ == "__main__":
    if test_connection(IP, PORT):
        print("Connection test passed.")
        face_recognition(IP, PORT)
    else:
        print("Connection test failed.")
