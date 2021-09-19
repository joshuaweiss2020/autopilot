# -*- coding: utf-8 -*-
'''
 # 小车前、后、左、右、停
 # by Joshua
 # 2021.9.4
'''
import RPi.GPIO as GPIO
import time
import Adafruit_PCA9685
import json
# from urllib.request import urlretrieve
import urllib

import os


class MovingCar:

    def __init__(self):
        with open("../adr.json", "r") as f:
            self.IP = json.load(f)

        # 左边两轮引脚
        self.PWMA = 18
        self.AIN1 = 22
        self.AIN2 = 27
        # 右边两轮引脚
        self.PWMB = 23
        self.BIN1 = 25
        self.BIN2 = 24

        # 舵机
        self.LR = 5  # 左右
        self.UD = 4  # 上下

        self.setup()

        self.enable = False

    def set_servo_angle(self, channel, angle):
        '''舵机角度处理函数'''
        angle = 4096 * ((angle * 11) + 500) / 20000
        print("angle:", str(angle), " channel:", str(channel))
        self.pwm.set_pwm(channel, 0, int(angle))

    def isEnable(self):
        '''判断是否已初始化或销毁'''
        return self.enable

    def setup(self):
        # 初始化
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.AIN2, GPIO.OUT)
        GPIO.setup(self.AIN1, GPIO.OUT)
        GPIO.setup(self.PWMA, GPIO.OUT)

        GPIO.setup(self.BIN1, GPIO.OUT)
        GPIO.setup(self.BIN2, GPIO.OUT)
        GPIO.setup(self.PWMB, GPIO.OUT)

        self.L_Motor = GPIO.PWM(self.PWMA, 100)  # 实例化频率为100的PWM
        self.L_Motor.start(0)

        self.R_Motor = GPIO.PWM(self.PWMB, 100)
        self.R_Motor.start(0)

        # 初始化舵机
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)

        self.enable = True

    def car_up(self, speed, t_time):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN2, False)  # self.AIN2
        GPIO.output(self.AIN1, True)  # self.AIN1

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN2, False)  # BIN2
        GPIO.output(self.BIN1, True)  # BIN1
        time.sleep(t_time)

    def car_stop(self, speed=0,t_time=0):
        self.L_Motor.ChangeDutyCycle(0)
        GPIO.output(self.AIN2, False)  # self.AIN2
        GPIO.output(self.AIN1, False)  # self.AIN1

        self.R_Motor.ChangeDutyCycle(0)
        GPIO.output(self.BIN2, False)  # BIN2
        GPIO.output(self.BIN1, False)  # BIN1
        time.sleep(t_time)

    def car_down(self, speed, t_time):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN2, True)  # self.AIN2
        GPIO.output(self.AIN1, False)  # self.AIN1

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN2, True)  # BIN2
        GPIO.output(self.BIN1, False)  # BIN1
        time.sleep(t_time)

    def car_left(self, speed, t_time):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN2, True)  # self.AIN2
        GPIO.output(self.AIN1, False)  # self.AIN1

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN2, False)  # BIN2
        GPIO.output(self.BIN1, True)  # BIN1
        time.sleep(t_time)

    def car_right(self, speed, t_time):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN2, False)  # self.AIN2
        GPIO.output(self.AIN1, True)  # self.AIN1

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN2, True)  # BIN2
        GPIO.output(self.BIN1, False)  # BIN1
        time.sleep(t_time)


    def camera_left(self,speed,t_time=0):
        self.set_servo_angle(self.LR, 30)
        time.sleep(t_time)

    def camera_right(self,speed,t_time=0):
        self.set_servo_angle(self.LR, 150)
        time.sleep(t_time)

    def camera_down(self,speed,t_time=0):
        self.set_servo_angle(self.UD, 175)
        time.sleep(t_time)

    def camera_up(self,speed,t_time=0):
        self.set_servo_angle(self.UD, 80)
        time.sleep(t_time)

    def camera_reset(self,speed,t_time=0):
        self.set_servo_angle(self.LR, 90)
        time.sleep(1)
        self.set_servo_angle(self.UD, 90)
        time.sleep(1)
        self.camera_stop()

    def camera_lookRoad(self,speed,t_time=0):
        self.set_servo_angle(self.LR, 90)
        time.sleep(1)
        self.set_servo_angle(self.UD, 120)
        time.sleep(1)
        self.camera_stop()

    def camera_stop(self,speed=0,t_time=0):
        self.pwm.set_pwm(self.UD, 0, 0)
        self.pwm.set_pwm(self.LR, 0, 0)

    def camera_takePhoto(self,speed=0,t_time=0):
        '拍照'

        img_url = "http://{}:8080/?action=snapshot".format(self.IP)
        # print(img_url)
        dir = os.path.abspath('../.') + "/img"
        now_str = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        picName = now_str + '.jpg'
        work_path = os.path.join(dir, picName)
        # print(work_path)
        urllib.urlretrieve(img_url, work_path)
        with open("../picNames.txt", "a") as f:
            f.write(picName + "\n")

    def destroy(self,speed=0,t_time=0):
        self.enable = False
        self.camera_stop()
        self.L_Motor.stop()
        self.R_Motor.stop()
        GPIO.cleanup()

    # 根据方法名调用方法
    def callback(self, name, *args):
        method = getattr(self, name, None)
        if callable(method):
            print("call ", name)

            return method(*args)


# 测试
if __name__ == "__main__":
    m = MovingCar()
    try:
        m.callback("camera_left",3)

        # while True:
        #     m.car_up(30, 3)
        #     m.car_down(30, 3)
        #     m.car_stop(3)
        #     m.car_right(30, 3)
        #     m.car_left(30, 3)
    finally:
        m.destroy()
