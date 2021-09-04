# -*- coding: utf-8 -*-
'''
 # 在后台运行，用于接受客户端发送的命令并执行
 # by Joshua
 # 2021.9.4
'''

from SimpleXMLRPCServer import SimpleXMLRPCServer
import moveControl.move as move

class CtrlServer:
    def __init__(self):
        self.server = SimpleXMLRPCServer(("",8989))
        #self.server.register_instance(self)
        #self.server.serve_forever()

        # self.MovingCar = move.MovingCar()

# 测试
if __name__ == "__main__":
    ctrlServer = CtrlServer()
    movingCar = move.MovingCar()
    ctrlServer.server.register_instance(movingCar)
    print("Server is up....")
    ctrlServer.server.serve_forever()
    