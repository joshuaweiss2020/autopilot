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
    t1, binary = cv2.threshold(gray_img, 225, 255, cv2.THRESH_BINARY)
    # 查找轮廓
    image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours, img


def findTarget(contours, img):
    """找到路径中心点，返回x,y坐标"""
    savedFlag = 0  # 记录要保存图片的环节 0-画所有轮廓 1-画符合条件的轮廓 2-画找到导航点的轮廓

    target_cY = -1
    target_cX = -1
    target_idx = -1
    target_area = -1
    target_length = -1
    # center_cX = 320  # 480*640
    
    image_show = []

    for i in range(0, len(contours) - 1):
        length = int(cv2.arcLength(contours[i], True))  # 周长
        area = int(cv2.contourArea(contours[i], False))  # 面积
        points = len(contours[i])  # 轮廓点数
        area_rate = judgeByArea(contours[i])  # 轮廓面积与将其包围的最小矩形的面积之比
        # 设定符合轮廓的条件
        if points < 500 and 1000 < area < 10000 and length >= 180 and area_rate>0:
            savedFlag = 1
            cX, cY = findCenter(contours[i])
            # print("\n target_idx:",target_idx," target_length:",
            # target_length,"area:",target_area,"target_cY:",target_cY)
            # print(i, ":", len(contours[i]),"length:",length,"area:",area,"cX?",cX,"cY:",cY,"\n")
            drawAndSavePic(img, contours, cX, cY, str(i), length, area,area_rate)

            # 在轮廓中选取：1.较靠底部 2相同周长所围面积较大 3 不能离顶部太近
            if (cY > target_cY or (length < target_length and area > target_area)
                or (length / area < target_length / target_area)) and cY > 120:
                target_cY = cY
                target_cX = cX
                target_idx = i
                target_area = area
                target_length = length

        #########################标记#################
    if target_idx >= 0:  # 如果找到导航点
        savedFlag = 2
        image_show=drawAndSavePic(img, contours, target_cX, target_cY, str(target_idx), length, area, area_rate,isTarget=True)

        # cv2.imshow("img",img)
        # cv2.waitKey()
    ############################################
    if savedFlag == 0:
        image_show=drawAndSavePic(img, contours)

    return target_cX, target_cY,image_show


def makeOrder(target_cX, target_cY):
    """行动指令 大于0向右，小于0向左"""
    center_cX = 320  # 640*480 中点
    center_cY = 240

    if target_cX < 0 or abs(target_cX - center_cX) > 250:  # 未找到行进点,偏离超过250像素视为误识别
        return None, None
    else:
        return target_cX - center_cX, target_cY - center_cY


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


def judgeByArea(contour):
    """通过面积判断是否符合"""
    rect = cv2.minAreaRect(contour)

    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

    area1 = cv2.contourArea(contour, False)
    area2 = cv2.contourArea(box, False)
    if area2==0:
        return 0
    rev = (area1 / area2)  # 比较轮廓面积与将其包围的最小矩形的面积
    return rev


def drawAndSavePic(img, contours, cX=0, cY=0, idx=-1, length=-1, area=-1, area_rate=0,isTarget=False):
    # print("drawAndSavePic,idx:", idx)
    idx = int(idx)
    nextLine = 20  # 处理换行
    """画轮廓，并保存图片"""
    center_cX = 320
    cv2.drawContours(img, contours, -1, (255, 0, 0), 5)
    msg = "no match contours"

    if idx >= 0:
        cv2.circle(img, (cX, cY), 3, (0, 255, 0), -1)
        cv2.circle(img, (center_cX, cY), 3, (0, 0, 255), -1)
        msg = "possible points:" + str(idx)
    if isTarget:
        msg = " this is nav point:" + str(idx)
        nextLine = 40

    cv2.putText(img, msg, (cX + 20, cY + nextLine),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)



    if not isTarget:  # 如果未找到目标，则不保存
        return img

    print("idx:", idx, "points:", len(contours[idx]), "length:", length, "area:", area, "area_rate",area_rate,
          "cX:", cX, "cY:", cX, "msg:", msg)

    dir = os.path.abspath('../.') + "/img/AP"
    now_str = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    picName = now_str + '.jpg'
    work_path = os.path.join(dir, picName)
    cv2.imwrite(work_path, img)
    with open("../AP_picNames.txt", "a") as f:
        f.write(picName + "\n")
    # work_path = os.path.join(dir, "now.jpg")
    # cv2.imwrite(work_path, img)
#    cv2.imshow("autoPilot", img)
#    cv2.waitKey()
    return img


if __name__ == "__main__":
    path_name = "../img/debug"
    for root, dir, files in os.walk(path_name):
        for file in files:
            # file = "20210919_114238.jpg"

            img = cv2.imread(path_name + "/{}".format(file))

            c, img = imagePre(img)
            x, y = findTarget(c, img)
            print("x:", x, "y:", y)
            print(makeOrder(x, y))
    # cv2.imshow("debug", img)
    # cv2.waitKey()
