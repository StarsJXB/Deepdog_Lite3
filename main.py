#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author  : Xiaobo Jia, shuo Gao
# @time    : 2024/9/13 19:20
# @function: 集二维码识别、播报和动作于一体的基础四足机器人案例
# @version : V1.0

import pyttsx3
import cv2
import threading
import time
from Move import Move  # 引入之前定义的机器狗控制类


# 定义一个类 Demo，用于实现图像捕捉、QR 码识别、语音提示和控制机器狗
class Demo:
    def __init__(self):
        # 初始化摄像头
        print("[INFO] : < ====== camera init... =======>")
        self.cap = cv2.VideoCapture(0)  # 使用 OpenCV 捕获摄像头图像
        self.cap.set(3, 640)  # 设置摄像头宽度
        self.cap.set(4, 480)  # 设置摄像头高度
        time.sleep(2)  # 等待摄像头稳定
        print("[INFO] : < ====== camera init over =======>")

        # 初始化机器狗
        self.dog = Move()

        # 初始化语音引擎
        self.engine = pyttsx3.init()

        # 初始化二维码检测器
        self.qr_detector = cv2.QRCodeDetector()

        # 存储捕获的图像
        self.img = None

        # 设置语音引擎的语速属性
        self.rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', self.rate - 50)  # 减慢语速

        # 标志，表明语音引擎是否正在运行
        self.is_engine_running = False

        # 存储检测到的二维码内容
        self.data = ''

        # 创建一个新的线程，用于不断检测二维码并做出反应
        self.speak_thread = threading.Thread(target=self.speak_move, daemon=True)
        self.speak_thread.start()

    # 处理图像中的 QR 码，并通过语音引擎反馈
    def speak_move(self):
        while True:
            # 当捕获到图像时
            if self.img is not None:
                # 尝试检测和解码 QR 码
                self.data, points, _ = self.qr_detector.detectAndDecode(self.img)

                # 如果检测到 QR 码
                if self.data:
                    # 如果语音引擎未运行，读取并反馈 QR 码内容
                    if not self.is_engine_running:
                        self.engine.say('I got it: ' + self.data)
                        self.is_engine_running = True
                        self.engine.runAndWait()  # 等待语音播报完成
                        self.is_engine_running = False

                        # 机器狗点头
                        self.dog.nod()
                else:
                    # 如果未检测到 QR 码，提示重试并让机器狗摇头
                    if not self.is_engine_running:
                        self.engine.say('Retrying')
                        self.is_engine_running = True
                        self.engine.runAndWait()
                        self.is_engine_running = False

                        # 机器狗摇头
                        self.dog.shake()

            # 避免忙等，延时 1 秒
            time.sleep(1)

    # 主函数，捕获摄像头的实时图像并显示
    def main(self):
        while True:
            # 从摄像头获取一帧图像
            ret, self.img = self.cap.read()
            if not ret:
                continue  # 如果没有获取到图像，继续等待

            # 显示图像窗口
            cv2.imshow('img', self.img)

            # 按下 'q' 键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # 释放摄像头并关闭所有窗口
        self.cap.release()
        cv2.destroyAllWindows()


# 程序入口，实例化 Demo 类并启动主程序
if __name__ == '__main__':
    dog = Demo()
    dog.main()
