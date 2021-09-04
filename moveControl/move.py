# -*- coding: utf-8 -*-
'''
 # 小车前、后、左、右、停
 # by Joshua
 # 2021.9.4
'''
import RPi.GPIO as GPIO
import time


class MovingCar:

    def __init__(self):
        # 左边两轮引脚
        self.PWMA = 18
        self.AIN1 = 22
        self.AIN2 = 27
        # 右边两轮引脚
        self.PWMB = 23
        self.BIN1 = 25
        self.BIN2 = 24
        
        self.setup()


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

    def t_up(self, speed, t_time):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN2, False)  # self.AIN2
        GPIO.output(self.AIN1, True)  # self.AIN1

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN2, False)  # BIN2
        GPIO.output(self.BIN1, True)  # BIN1
        time.sleep(t_time)

    def t_stop(self, t_time):
        self.L_Motor.ChangeDutyCycle(0)
        GPIO.output(self.AIN2, False)  # self.AIN2
        GPIO.output(self.AIN1, False)  # self.AIN1

        self.R_Motor.ChangeDutyCycle(0)
        GPIO.output(self.BIN2, False)  # BIN2
        GPIO.output(self.BIN1, False)  # BIN1
        time.sleep(t_time)

    def t_down(self, speed, t_time):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN2, True)  # self.AIN2
        GPIO.output(self.AIN1, False)  # self.AIN1

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN2, True)  # BIN2
        GPIO.output(self.BIN1, False)  # BIN1
        time.sleep(t_time)

    def t_left(self, speed, t_time):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN2, True)  # self.AIN2
        GPIO.output(self.AIN1, False)  # self.AIN1

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN2, False)  # BIN2
        GPIO.output(self.BIN1, True)  # BIN1
        time.sleep(t_time)

    def t_right(self, speed, t_time):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN2, False)  # self.AIN2
        GPIO.output(self.AIN1, True)  # self.AIN1

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN2, True)  # BIN2
        GPIO.output(self.BIN1, False)  # BIN1
        time.sleep(t_time)

    def destroy(self):
        self.L_Motor.stop()
        self.R_Motor.stop()
        GPIO.cleanup()


    def hello(self,cmd):
        print("cmd:",cmd)

# 测试
if __name__ == "__main__":
    m = MovingCar()
    try:
        while True:
            m.t_up(30, 3)
            m.t_down(30, 3)
            m.t_stop(3)
            m.t_right(30, 3)
            m.t_left(30, 3)
    finally:
        m.destroy()
