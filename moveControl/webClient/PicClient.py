# -*- coding: utf-8 -*-
'''
 # 客户端发送命令
 # by Joshua
 # 2021.9.4
'''

from xmlrpc.client import ServerProxy
# import moveControl.move
import time
import json
from urllib.request import urlretrieve
import os


class PicClient:
    def __init__(self):

        with open("adr.json", "r") as f:
            self.IP = json.load(f)
        self.server = ServerProxy('http://{}:9090'.format(self.IP))

    def callAction(self,action,speed=30,t_time=0):
        '''调用服务器端动作
          小车action为 ：car_up car_down car_stop car_left car_right
          摄像头action为：camera_up camera_down camera_stop camera_left camera_right
        '''

        #判断相关GPIO接口是否重置过
#        if not self.server.isEnable():
#            try:
#                self.server.setup()
#            except Exception:
#                pass
#
        rev = self.server.callback(action,speed,t_time)
        return rev






    def callCmd(self,cmd):

        self.server.setup()
        self.server.t_up(30, 3)
        # time.sleep(3)
        self.server.destroy()





        # self.server.t_stop(3)


# 测试
if __name__ == "__main__":
    print("start")
    p = PicClient()
    print("init finished")
    s=p.callAction("getLastestPic",0,0)
    print(s)
    # ctrlClient.callAction("camera_left",1)
    # ctrlClient.callAction("camera_stop", 0)
    # ctrlClient.callAction("camera_reset")
    # IP = "192.168.1.100"
    # with open("adr.json", "w") as f:
    #     json.dump(IP,f)


#    with open("../adr.json", "r") as f:
#        IP = json.load(f)
#        print(IP)
#
#    img_url = "http://{}:8080/?action=snapshot".format(IP)
#    print(img_url)
#    dir = os.path.abspath('.') + "\\img"
#    now_str = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
#    # dir = "C:\\"
#    picName = now_str+'.jpg'
#    work_path = os.path.join(dir, picName)
#    print(work_path)
#    urlretrieve(img_url, work_path)
#
#    with open("picNames.txt","a") as f:
#        f.write(picName + "\n")
#
#    with open("picNames.txt","r") as f:
#        lines = f.read().splitlines()
#        print(lines)
#
#    print(int(len(lines)/3))


    # picNameDic = {"name":[picName]}
    # with open("picNames.json", "a") as f:
    #     json.dump(picNameDic, f)
    #
    # with open("picNames.json", "r") as f:
    #     s = json.load(f)
    #     print(s)




