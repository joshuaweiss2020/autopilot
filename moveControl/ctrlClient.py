# -*- coding: utf-8 -*-
'''
 # 客户端发送命令
 # by Joshua
 # 2021.9.4
'''
#from xmlrpclib import ServerProxy
from xmlrpc.client import ServerProxy
# import moveControl.move
import time

class CtrlClient:
    def __init__(self):
        self.server = ServerProxy('http://192.168.137.158:8989')


    def callCmd(self,cmd):

        self.server.setup()
        self.server.t_up(30, 3)
        # time.sleep(3)
        self.server.destroy()





        # self.server.t_stop(3)


# 测试
if __name__ == "__main__":
    ctrlClient = CtrlClient()
    ctrlClient.callCmd("hello")


