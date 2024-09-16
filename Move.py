#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author  : Xiaobo Jia, shuo Gao
# @time    : 2024/9/13 19:20
# @function: 控制机器狗
# @version : V1.0

import struct
import socket
import time
import threading


# 运动类，用于控制机器狗的各种运动行为
class Move:
    def __init__(self, dst=("192.168.1.120", 43893)):
        # 设置 UDP 套接字，用于与机器狗通信
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 设置目标主机的 IP 和端口号
        self.dst = dst

        # 心跳包控制开关
        self.stop_heartbeat = False

        # 开启心跳线程，保持与机器狗的通信
        self.start_heartbeat()

        # 设置初始速度
        self.speed = 20000

        # 初始化机器狗
        self.dog_init()

    # 机器狗的初始化方法
    def dog_init(self):
        print('Dog init ...')
        # 让机器狗站立
        self.stand_up()
        time.sleep(2)
        # 切换为手动模式
        self.hand_mode()
        time.sleep(2)
        print('Dog init done')

    # 心跳包发送，保持与机器狗的连接
    def start_heartbeat(self):
        def heart_exchange():
            # 心跳包数据格式：发送0x21040001和两个0值
            pack = struct.pack('<3i', 0x21040001, 0, 0)
            while True:
                if self.stop_heartbeat:
                    return
                # 每次发送心跳包
                self.send(pack)
                time.sleep(0.25)  # 4Hz 的频率发送心跳包

        # 创建心跳包线程，持续发送心跳
        heart_exchange_thread = threading.Thread(
            target=heart_exchange,
            daemon=True  # 守护线程，主程序结束时自动结束
        )
        # 启动心跳线程
        heart_exchange_thread.start()

    # 发送UDP数据包给机器狗
    def send(self, pack):
        self.socket.sendto(pack, self.dst)

    # 让机器狗站起来
    def stand_up(self):
        print('[INFO]: Dog is ready to stand up...')
        # 发送站立指令
        self.send(struct.pack('<3i', 0x21010202, 0, 0))

    # 让机器狗坐下
    def sit(self):
        # 发送坐下指令
        self.send(struct.pack('<3i', 0x21010202, 0, 0))
        print('[INFO]: Dog has sat down')

    # ------------ 移动功能 ------------

    # 机器狗前进
    def forward(self, run_time):
        print('[INFO]: go')
        cTime = time.time()
        # 持续发送前进指令，直到运行时间达到设定值
        while time.time() - cTime <= run_time:
            self.send(struct.pack('<3i', 0x21010130, self.speed, 0))

    # 机器狗后退
    def back(self, run_time):
        print('[INFO]: back')
        cTime = time.time()
        # 持续发送后退指令，直到运行时间达到设定值
        while time.time() - cTime <= run_time:
            self.send(struct.pack('<3i', 0x21010130, -self.speed, 0))

    # 机器狗向左平移
    def left(self, run_time):
        print('[INFO]: left')
        cTime = time.time()
        # 持续发送左移指令，直到运行时间达到设定值
        while time.time() - cTime <= run_time:
            self.send(struct.pack('<3i', 0x21010131, -self.speed, 0))

    # 机器狗向右平移
    def right(self, run_time):
        print('[INFO]: right')
        cTime = time.time()
        # 持续发送右移指令，直到运行时间达到设定值
        while time.time() - cTime <= run_time:
            self.send(struct.pack('<3i', 0x21010131, self.speed, 0))

    # 机器狗原地向左转
    def turn_left(self, run_time):
        print('[INFO]: turn left')
        cTime = time.time()
        # 持续发送左转指令，直到运行时间达到设定值
        while time.time() - cTime <= run_time:
            self.send(struct.pack('<3i', 0x21010135, -self.speed, 0))

    # 机器狗原地向右转
    def turn_right(self, run_time):
        print('[INFO]: turn right')
        cTime = time.time()
        # 持续发送右转指令，直到运行时间达到设定值
        while time.time() - cTime <= run_time:
            self.send(struct.pack('<3i', 0x21010135, self.speed, 0))

    # ------------ 模式切换 ------------

    # 切换为手动模式
    def hand_mode(self):
        # 发送切换到手动模式的指令
        self.send(struct.pack('<3i', 0x21010D06, 0, 0))
        print('[INFO]: change to hand mode')

    # 切换为自动模式
    def auto_mode(self):
        # 发送切换到自动模式的指令
        self.send(struct.pack('<3i', 0x21010D05, 0, 0))
        print('[INFO]: change to auto mode')

    # 停止心跳线程
    def stop(self):
        self.stop_heartbeat = True

    # 机器狗点头功能，前后移动模拟点头
    def nod(self):
        # 切换为自动模式
        self.auto_mode()
        time.sleep(2)
        # 机器狗前后移动两次
        for _ in range(2):
            self.forward(1)
            self.back(1)

    # 机器狗摇头功能，左右平移模拟摇头
    def shake(self):
        # 切换为自动模式
        self.auto_mode()
        time.sleep(2)
        # 机器狗左右移动两次
        for _ in range(2):
            self.left(1)
            self.right(1)
