# -*- coding: UTF-8 -*-
import json
from urllib import request
from bs4 import BeautifulSoup
import random
import threading

def thread(url):
    for i in range(10):
        response = request.urlopen(url)
        text = response.read()
        print(i)

if __name__ == '__main__' :
            '''
            url=[]
            url.append("https://www.etymonline.com/word/fuck")
            url.append("https://www.baidu.com")
            url.append("https://www.taobao.com")
            url.append("https://www.bilibili.com")
            url.append("https://www.zhihu.com/")
            url.append("https://www.douyu.com")

            myurl = "http://localhost/api/?url="
            for i in range(1000):
                r=int(random.random()*len(url))
                aurl=url[r]
                t=threading.Thread(target=thread,args=(aurl,))
'''
            url="http://localhost/api/?url=https://www.etymonline.com/word/fuck&&session=ymc2roc1"
            response = request.urlopen(url)
            text = response.read().decode()
            text=json.loads(text)
            for key in text:
                print(text[key])







