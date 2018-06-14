# -*- coding: UTF-8 -*-
import json
from urllib import request
from bs4 import BeautifulSoup
import random
import threading


x=[0]
mutex=threading.Lock()

def thread(url):
    for i in range(10):
        response = request.urlopen(url)
        text = response.read()
    global x,mutex
    mutex.acquire()
    x[0]=x[0]+10
    print(x[0])
    print(text)
    print(url)
    mutex.release()


if __name__ == '__main__' :

            url=[]
            url.append("https://www.etymonline.com/word/jack")
            url.append("https://www.baidu.com")
            url.append("https://www.taobao.com")
            url.append("https://www.bilibili.com")
            url.append("https://www.zhihu.com/")
            url.append("https://www.douyu.com")
            url.append("https://sakai.sustc.edu.cn")
            url.append("https://github.com/")
            url.append("https://weibo.com/")

            myurl = "http://localhost/api/?url="
            list1=[]
            for i in range(100):
                r=int(random.random()*len(url))
                aurl=url[r]
                t=threading.Thread(target=thread,args=(aurl,))
                list1.append(t)
            for i in list1:
                i.start()
                i.join()









