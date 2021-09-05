# -*- coding: utf-8 -*-
'''
 # 客户端发送命令
 # by Joshua
 # 2021.9.4
'''

from xmlrpc.client import ServerProxy
# import moveControl.move
import time

class CtrlClient:
    def __init__(self):
        self.server = ServerProxy('http://192.168.1.100:8989')


    def callAction(self,action,speed=30,t_time=0):
        '''调用服务器端动作
          小车action为 ：car_up car_down car_stop car_left car_right
          摄像头action为：camera_up camera_down camera_stop camera_left camera_right
        '''

        #判断相关GPIO接口是否重置过
        if not self.server.isEnable():
            try:
                self.server.setup()
            except Exception:
                pass

        self.server.callback(action,speed,t_time)







    def callCmd(self,cmd):

        self.server.setup()
        self.server.t_up(30, 3)
        # time.sleep(3)
        self.server.destroy()





        # self.server.t_stop(3)


# 测试
if __name__ == "__main__":
    ctrlClient = CtrlClient()
    # ctrlClient.callAction("camera_left",1)
    # ctrlClient.callAction("camera_stop", 0)
    ctrlClient.callAction("camera_reset")


