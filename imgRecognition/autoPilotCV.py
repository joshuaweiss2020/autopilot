import cv2
import numpy as np
import os


def findCenter(c,image,i):

    # ?????
    # for c in cnts:
        # ??????????? ???????????????????????????????????????????????????????????????????x?y?????????????????
        cX,cY=0,0
        M = cv2.moments(c)
        if M["m00"]!=0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        # ???????????
        #     cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        # cv2.circle(image, (cX, cY), 3, (0, 255, 0), -1)
        # cv2.putText(image, str(i), (cX - 20, cY - 20),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        return cX,cY

imgFiles = []
# if 1:
path_name = "../img_res/img_b"
for root,dir,files in os.walk(path_name):
    for file in files:
        # file = "20210919_114724.jpg"


        img = cv2.imread(path_name + "/{}".format(file))
        # img = cv2.imread("img_res/20210911_161104.jpg")




        # cv2.imshow("1", img)
        # cv2.waitKey()

        # ????
        filter = cv2.bilateralFilter(img, 20, 120, 100)
        # ????
        # filter = cv2.medianBlur(img, 5)
        # ????
        # filter = cv2.GaussianBlur(img,(9,9),0,0)
        # cv2.imshow("2", filter)
        # cv2.waitKey()
        # ????
        gray_img = cv2.cvtColor(filter, cv2.COLOR_RGB2GRAY)
        # cv2.imshow("3", gray_img)
        # cv2.waitKey()
        # ??????????127???220?????
        t1, binary = cv2.threshold(gray_img, 230, 255, cv2.THRESH_BINARY)
        # cv2.imshow("4", binary)
        # cv2.waitKey()
        # ???
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        cY_max = 0
        target_cX =0
        target_idx = -1
        target_area = 0
        target_length = 0

        center_cX = 320  #480*640
        # print("image:",img.shape)

        for i in range(0, len(contours) - 1):
            length = int(cv2.arcLength(contours[i], True))
            area = int(cv2.contourArea(contours[i], False))

            ##########################??
            if 0:
                if length>10:
                    cv2.drawContours(img, contours[i], -1, (0, 0, 255), 5)
                    cX,cY=0,0
                    cX, cY = findCenter(contours[i], img, i)
                    cv2.putText(img, str(i), (cX - 20, cY - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    print("test:",i, ":", len(contours[i]), "length:", length, "area:", area, "cX?", cX, "cY:", cY)

            #############################################
        #
            if len(contours[i]) < 500 and area>1000 and area<10000 and length>=180 :
        #         #
        #
                cX,cY = findCenter(contours[i],img,i)
                print("\ntarget_idx:",target_idx," target_length:",target_length,"area:",target_area,"cy_max:",cY_max)
                print(i, ":", len(contours[i]),"length:",length,"area:",area,"cX?",cX,"cY:",cY,"\n")

                #????????????? ???????????? ???????200

                if (cY>cY_max or (length<target_length and area>target_area)
                    or (length/area<target_length/target_area)) and cY>120:
                    cY_max = cY
                    target_cX = cX
                    target_idx = i
                    target_area = area
                    target_length = length

        if target_idx>=0:
            cv2.drawContours(img, contours[target_idx], -1, (0, 0, 255), 5)
            cv2.circle(img, (target_cX, cY_max), 3, (0, 255, 0), -1)
            cv2.putText(img, str(target_idx), (target_cX - 20, cY_max - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            print("idx:",target_idx, "points:", len(contours[target_idx]), "length:", target_length, "area:", target_area, "cX:", cX, "cY:", cY)

            cv2.circle(img, (center_cX, cY_max), 3, (0, 0, 255), -1)

            if center_cX < target_cX:
                msg = "turn right:" + str(target_cX-center_cX)
            elif center_cX > target_cX:
                msg = "turn left:" + str(center_cX - target_cX)
            else:
                msg = "in center!"

            print(msg)
            cv2.putText(img, str(msg), (200,200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)

        else:
            print("out of range")
            cv2.putText(img, "can't find road!!", (400-20, 300 - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)



        cv2.imshow(file, img)
        cv2.waitKey()

cv2.destroyAllWindows()
#132 147 151
#64 : 234 length: 244.76955199241638 area: 2997.0 cX? 121 cY: 168
#55 : 164 length: 189.68123936653137 area: 1013.0 cX? 222 cY: 387