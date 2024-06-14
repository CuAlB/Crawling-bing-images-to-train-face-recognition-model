# Crawling-bing-images-to-train-face-recognition-model
Crawling bing images by python crawler technique to train face recognition model, and then turn on the computer camera for facial recognition module.

分为三个模块,

main.py用于在图片网站进行搜索相应人物并保存到本地,这里使用的网站是bing图片

face_extract.py用于将保存到本地的图片通过级联识别器进行提取人脸,并保存到imgs文件夹

face_match.py同时进行将imgs中的人脸转为灰度图存储在face文件夹中并用灰度人脸图片进行模型训练,训练结束后打开摄像头开始进行面部捕获和识别.

级联识别器xml文件已经附在目录中,只需要在你的编译器中安装对应的库即可运行,当然还需要一个摄像头

It is divided into three modules.

main.py is used to search the corresponding characters in the picture website and save them locally, the website used here is bing picture.

face_extract.py is used to extract the face from the saved image by cascade recogniser and save it to imgs folder.

face_match.py at the same time will be imgs in the face to grey-scale map stored in the face folder and grey-scale face images for model training, after the end of the training to open the camera to start face capture and recognition.

The cascade recogniser xml file is already attached to the directory, you just need to install the corresponding library in your compiler to run it, and of course a webcam
