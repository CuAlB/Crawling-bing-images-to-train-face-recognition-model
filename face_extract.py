# 获取小头像信息
import cv2
import os

dirs = os.listdir("imgs")
for j, dir in enumerate(dirs):
    print(dir)
    # 判断是否有存储头像的路径
    file_path = "face/%s" % str(dir)
    # 为方便展示,已存在的数据不会被替换掉
    if os.path.exists(file_path):
        print(str(dir), '已经存在,若想重新导入请删除该文件夹')
        continue
    else:
        os.makedirs(file_path)
    num = 0
    files = os.listdir('imgs/%s' % dir)  # 读入文件夹
    num_img = len(files)  # 统计文件夹中的文件个数
    for i in range(1, num_img):
        image = cv2.imread('imgs/%s/%d.jpg' % (dir, i))
        if image is None:
            print('本地图像无法打开')
            continue
        gray = cv2.cvtColor(image, code=cv2.COLOR_BGR2GRAY)
        # 数据参数 CascadeClassifier—级联分类器
        # 是OpenCV库中预训练的用于面部检测的机器学习算法(Haar特征值反映了图像的灰度变化情况)
        face_detector = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        # 进行数据对比:minNeighbors = 每一个目标至少要被检测 -整数
        # 每个候选矩形应保留近邻数目的最小值。这个参数将会影响检测到目标的质量。数值越大，检测到的目标越少，但质量越高。3~6是比较好的值
        face_01 = face_detector.detectMultiScale(gray, minNeighbors=4)  # 返回值为头像左下角坐标,长与宽
        # 绘制矩形人脸检测
        print("第%d张图片===:" % i, face_01)
        if len(face_01) is 0:
            print("未检测到头像")
        else:
            print("检测到头像")
            for x, y, w, h in face_01:  # x,y为左下角坐标,w->wide宽,h->high高
                x_face = gray[y:y + h, x:x + w]
                x_face = cv2.resize(x_face, dsize=(200, 200))
                flag = cv2.imwrite("%s\%d.jpg" % (file_path, num), x_face)
                if flag is True:
                    print("保存成功:%d" % num)
                    num += 1
                else:
                    print("保存失败")   # 该情况基本不会发生
