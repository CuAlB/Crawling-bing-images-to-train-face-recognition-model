# -*- coding = utf-8 -*-
# @Time : 2023/11/25 13:15
# @Author :55221324佟禹澎
# @File : face_extract.py
# @Software: PyCharm
import os
import urllib
import re
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}
# header值由我的谷歌浏览器得到
url = "https://cn.bing.com/images/?q={0}&form=QBIR&first={1}"
# 可更改q的值来变换查询内容,form=QBIR为默认,未找到关于这个参数的相关信息
# 经测试,bing图片在url中即使修改count与relp的值也无法改变页面图片数,每页图片恒定为35张
# first代表展示的首个图片,若想访问更多图片,我们通过改变first的方式切换首图片即可

def getImage(url, who):
    global count_pic
    # 从原图url中将原图保存到本地
    try:
        # urlretrieve可以从链接(必须是图片链接,图片后缀结尾的链接)下载图片到本地
        urllib.request.urlretrieve(url, './imgs/{}/'.format(who) + str(count_pic + 1) + '.jpg')
    except Exception as e:
        print("本张图片获取异常，跳过...")
        return 0
    else:
        print("图片+1,保存成功 ", "共有" + str(count_pic + 1) + " 张图")
        return 1


def findImgUrlFromHtml(html, target, who):
    # 从图片搜索页面找到原图的url
    global count_pic    # 为保证count_pic值可修改,将其作为全局变量传递
    soup = BeautifulSoup(html, "lxml")
    # 使用lxml解析网页
    link_list = soup.find_all("a", class_='iusc')
    # "a"代表HTML中的<a>标签，也就是超链接标签
    # BeautifulSoup会查找所有类名为"iusc"的<a>标签,里面有我们需要的murl标签
    for link in link_list:
        result = re.search(r'"murl":"(https?://[^"]+)"', str(link))     # murl标签后面就是原图链接,得到正则表达式 s?很重要
        if result is None:
            print('该图片正则表达式不匹配')
            continue
        url = result.group(1)
        # 打开高清图片网址,保存到文件夹中
        flag = getImage(url, who)
        # 若找到计数器count++
        if flag == 1: count_pic += 1
        # 一旦图片数目达标,返回完成标志1
        if count_pic >= target:
            return 1
    # 完成一页,但未完成任务,返回未完成标志0
    return 0


def getStartHtml(key, first):
    # 构造链接,得到特定first值的网页链接
    page = urllib.request.Request(url.format(key, first), headers=header)
    # 找到第first页的响应对象
    html = urllib.request.urlopen(page)
    # 使用urlopen通过响应对象获取链接
    return html


name = input('想要谁的图片?\n')  # 图片关键词
who = '_'.join(lazy_pinyin(name))  # 由于图片提取函数以及人脸匹配函数无法访问中文路径,必须转换成拼音保存
target = int(input('想要几张?\n'))
path = f'./imgs/{who}'  # 图片保存路径
key = urllib.parse.quote(name)
# 我们需要将文字内容转换成url形式,以添加到url中
count_pic = 0  # 全局变量
if not os.path.exists(path):
    # 若路径不存在,则创建路径
    os.makedirs(path)
flag = 0
first = 1
# flag为任务完成标志,初始未完成flag置0
while flag != 1:
    html = getStartHtml(key, first)
    flag = findImgUrlFromHtml(html, target, who)
    # 进行对一页的爬取
    first += 35
    # 无论是否完成任务,首个图片+35即可,因为完成了会退出循环
