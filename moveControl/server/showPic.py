# -*- coding: utf-8 -*-

import move as mv
import cv2
import time
import os
import random

dir = os.path.abspath('../.') + "/img/AP"

def getLastestPic():
    """取得最新一张在AP状态下保存的图片名称"""
    with open("../AP_picNames.txt", "r") as f:
        filenames = f.read().splitlines()
        filenames.reverse()
#        i = random.randint(0,len(filenames)-1)
#    print(filenames[0])
    return filenames[0]

if __name__ == "__main__":


        while True:
            picFile = getLastestPic()
            image = cv2.imread(dir + "/{}".format(picFile))
            cv2.imshow("monitor",image)
            cv2.waitKey(1000)
            print(picFile)
#            time.sleep(3)

