# -*- coding: utf-8 -*-
'''
 # 在后台运行，用于接受客户端发送的命令并执行
 # by Joshua
 # 2021.9.4
'''

from SimpleXMLRPCServer import SimpleXMLRPCServer
import move
import json
import socket
import cv2
class CtrlServer:
    def __init__(self):
        with open("../adr.json", "r") as f:
            self.IP = json.load(f)
        self.server = SimpleXMLRPCServer((self.IP,8989),allow_none=True)
        #self.server.register_instance(self)
        #self.server.serve_forever()

        # self.MovingCar = move.MovingCar()

# 测试
if __name__ == "__main__":
    # IP = "192.168.1.100"
    # with open("adr.json", "w") as f:
    #     json.dump(IP,f)
    ctrlServer = CtrlServer()
    movingCar = move.MovingCar()
   # movingCar.destroy()
#    movingCar.video_capture = cv2.VideoCapture(0)
#    movingCar.video_capture.release()
#    
#    print("video:", movingCar.video_capture.isOpened())
    ctrlServer.server.register_instance(movingCar)
    print("Server is up....")
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    print(ip)

    ctrlServer.server.serve_forever()

