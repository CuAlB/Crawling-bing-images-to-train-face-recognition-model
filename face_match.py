# -*- coding = utf-8 -*-
# @Time : 2023/11/27 14:52
# @Author :55221324佟禹澎
# @File : face_match.py
# @Software: PyCharm

# 人脸识别 - 主代码
import cv2
import os
import numpy as np
from playsound import playsound


def Get_faces():
    # 从face文件夹读取图片,转为灰度图,返回三个列表:对应人名,灰度图片,图片序号
    dirs = os.listdir("face")
    print(dirs)
    X = []  #
    Y = []  #
    for j, dir in enumerate(dirs):
        pics = os.listdir('face/%s' % dir)
        for pic in pics:
            image = cv2.imread('face/%s/%s' % (dir, pic))
            img_gray = cv2.cvtColor(image, code=cv2.COLOR_BGR2GRAY)
            resized_gray = cv2.resize(img_gray, dsize=(400, 400))
            print("读取/", dir, "/", pic)
            if len(str(image)) != 0:
                X.append(resized_gray)
                Y.append(j)
    return [X, Y, dirs]


X, Y, dirs = Get_faces()
print("本次即将学习以下人脸", dirs)
# 利用asarray将数据转化为ndarray->多维数组
X = np.asarray(X)
Y = np.asarray(Y)

# 我们采用三种算法中的LBPH算法,Local BInary Pattern Histogram (LBPH),即二进制模式直方图
# 经测试,create中默认参数就是最好的参数,只需在后续修改阈值即可
model = cv2.face.LBPHFaceRecognizer_create(grid_x=8, grid_y=8)
model.train(X, Y)
print("学习完毕,总共吃了%d张图片" % len(Y))

Video_face = cv2.VideoCapture(0)   # 参数0 代表从摄像头中读取视频
# xml文件,原理同face_extract,用于捕获视频中出现的人脸
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
# while循环调取视频某一帧
while True:
    try:
        flag, frame = Video_face.read()    # read返回是否读取成功和该帧图片
        gray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)    # 将该帧图片转为灰度图像
        faces = face_detector.detectMultiScale(gray, 1.1, 3)    # 从灰度图像中截取人脸->faces,包含左下角坐标,区域长宽

        if len(faces) is 0:
            # 当摄像头存在但未开启状态,flag是true的,所以还要通过faces是否空来判断
            print("未检测到头像")
        else:
            print("检测到头像")
            # for循环遍历该帧图片中所有出现的人脸
            for x, y, w, h in faces:
                cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=[0, 0, 255], thickness=2)    # 绘制正方形,框住人脸
                face = gray[y:y + h, x:x + w]   # 截断获得包含人脸数据的数组
                print("摄像头捕获到头像尺寸为:", face.shape, "修改成400*400")
                face_1 = cv2.resize(face, dsize=(400, 400))
                # 开始对比
                result = model.predict(face_1)  # 用训练好的模型中predict函数预测人脸结果,result[0]保存对应序号,result[1]保存置信度
                print("对比返回结果：")
                print(f'该人脸是：{dirs[result[0]]},置信度为:{result[1]}')
                if dirs[result[0]] == 'ke_bi' and result[1] < 40:
                    cv2.destroyAllWindows()
                    kebi=cv2.imread('laoda.jpg')
                    cv2.imshow('waaaaaaa', kebi)
                    cv2.waitKey(1000)
                    playsound("laoda.mp3")
                a1 = dirs[result[0]]
                if result[1] > 65 or (dirs[result[0]] == 'ke_bi' and result[1] > 40):  # 一般置信度小于65基本可信
                    a1 = "unmatched"
                    # 将名称放在框上
                cv2.putText(frame, a1, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, [255, 0, 0], 2)
            print("=======================CuAlB分割线=======================")
        cv2.imshow('face', frame)   # 打开摄像头
        try:
            cv2.waitKey(100)
        except KeyboardInterrupt:
            break
    except KeyboardInterrupt:
        break
cv2.destroyAllWindows()