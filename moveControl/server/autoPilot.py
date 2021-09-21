# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import os
import time


def imagePre(img):
    """图像预处理，返回轮廓,原图"""
    # 双边滤波 d=20滤波直径 sigmaColor=120 颜色差值 sigmaSpace=100
    filter = cv2.bilateralFilter(img, 20, 120, 100)
    # 灰度处理
    gray_img = cv2.cvtColor(filter, cv2.COLOR_RGB2GRAY)
    # 二值化处理 thresh=230 去高光 maxVal=255(白）
    t1, binary = cv2.threshold(gray_img, 230, 255, cv2.THRESH_BINARY)
    # 查找轮廓
    image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours, img


def findTarget(contours, img):
    """找到路径中心点，返回x,y坐标"""
    target_cY = -1
    target_cX = -1
    target_idx = -1
    target_area = -1
    target_length = -1
    # center_cX = 320  # 480*640

    for i in range(0, len(contours) - 1):
        length = int(cv2.arcLength(contours[i], True))  # 周长
        area = int(cv2.contourArea(contours[i], False))  # 面积
        points = len(contours[i])  # 轮廓点数

        # 设定符合轮廓的条件
        if points < 500 and 1000 < area < 10000 and length >= 180:
            cX, cY = findCenter(contours[i])
            # print("\n target_idx:",target_idx," target_length:",
            # target_length,"area:",target_area,"target_cY:",target_cY)
            # print(i, ":", len(contours[i]),"length:",length,"area:",area,"cX?",cX,"cY:",cY,"\n")

            # 在轮廓中选取：1.较靠底部 2相同周长所围面积较大 3 不能离顶部太近
            if (cY > target_cY or (length < target_length and area > target_area)
                or (length / area < target_length / target_area)) and cY > 120:
                target_cY = cY
                target_cX = cX
                target_idx = i
                target_area = area
                target_length = length

        #########################标记#################
    if target_idx >= 0:  # 如果找到
        center_cX =320
        cv2.drawContours(img, contours[target_idx], -1, (0, 0, 255), 5)
        cv2.circle(img, (target_cX, target_cY), 3, (0, 255, 0), -1)
        cv2.putText(img, str(target_idx), (target_cX - 20, target_cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        print("idx:", target_idx, "points:", len(contours[target_idx]), "length:", target_length, "area:", target_area,
              "cX:", target_cX, "cY:", target_cX)

        cv2.circle(img, (center_cX, target_cY), 3, (0, 0, 255), -1)

        dir = os.path.abspath('../.') + "/img/AP"
        now_str = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        picName = now_str + '.jpg'
        work_path = os.path.join(dir, picName)
        cv2.imwrite(work_path,img)
        with open("../AP_picNames.txt", "a") as f:
            f.write(picName + "\n")
        work_path = os.path.join(dir, "now.jpg")
        cv2.imwrite(work_path, img)

        # cv2.imshow("img",img)
        # cv2.waitKey()
    ############################################

    return target_cX, target_cY


def makeOrder(target_cX, target_cY):
    """行动指令 大于0向右，小于0向左"""
    center_cX = 320  # 640*480 中点
    center_cY = 240

    if target_cX < 0 or abs(target_cX - center_cX) > 150:  # 未找到行进点,偏离超过150像素视为误识别
        return None,None
    else:
        return target_cX - center_cX,target_cY - center_cY


def findCenter(c):
    """寻找中心点"""
    cX, cY = 0, 0
    M = cv2.moments(c)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    # ???????????
    #     cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    # cv2.circle(image, (cX, cY), 3, (0, 255, 0), -1)
    # cv2.putText(image, str(i), (cX - 20, cY - 20),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    return cX, cY
