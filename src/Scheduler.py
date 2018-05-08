#coding=utf-8
import time
import re
import threading
import DBUtils
from IP_Queue import *
from urllib import request,parse,error
from http import cookiejar
import queue




class Scheduler:

    def __init__(self,url,headers={'User-agent':'Mozilla/5.0'},time_max=1,time_delay=1,request_con=1,session=False):#任务调度
        # url 为访问的地址， headers 为报头， time_max 为每个ip最大访问数， time_delay 为访问间隔, request_con 为任务并发数

        global Queue,count,Max_count,mutex

        mutex=threading.Lock()  #计数锁
        Queue=IP_Queue()  # 初始化可用ip队列
        count=0          #初始化报错计数

        Max_count= request_con * time_max
        if(request_con<5):
            Max_count=5      #初始化报错最大值

        if not re.match(r'^https?:/{2}\w.+$', url):  # 若url不合法则返回error
            print("error")
            return

        thread_list=[]
        for i in range(request_con):

            while (True):
                try:
                    proxy_ip = Queue.get_ip(block = False)  # 从可用ip队列中取出首ip,取出失败则将sleep几秒
                    break
                except queue.Empty:
                    pass
                time.sleep(3)   #取出失败
                if (count >= Max_count):
                    print("shit!")
                    return

            t = threading.Thread(target=Visit_Thread, args=(url, headers, time_max, time_delay, proxy_ip, session))
            t.start()
            thread_list.append(t)
            
        for t in thread_list:
            t.join()
        if(count>=Max_count):
            print("shit!")






def visit(url,headers,proxy_ip,cookie=cookiejar.CookieJar()):#单次访问网站

    for key in proxy_ip:
        ip = proxy_ip[key]
    try:
        proxy_handler = request.ProxyHandler(proxy_ip)  #创建代理处理器
        cookie_handler = request.HTTPCookieProcessor(cookie)    #创建cookie处理器

        opener = request.build_opener(proxy_handler,cookie_handler)     #创建opener
        RequestA = request.Request(url)

        for key in headers.keys():
            RequestA.add_header(key,headers[key])    #添加报文头部

        response_time = time.time()
        response = opener.open(RequestA) #访问
        response_time = time.time() - response_time #响应时间

    except (ConnectionRefusedError,TimeoutError)as e :
        response_time=-1
        sentence=time.asctime( time.localtime(time.time()) )+" use "+ip+" requested "+url+" failed. "
        print(sentence+" Error is "+ e.message)

        return False
    except error.URLError:
        sentence = time.asctime(time.localtime(time.time())) + " use " + ip + " requested " + url + " failed. "
        print(sentence+" Error is URLError")
        return False
    sentence = time.asctime(time.localtime(time.time())) + " use " + ip + " requested " + url + " success. "
    print(sentence)
    return cookie



def Visit_Thread(url,headers,time_max,time_delay,proxy_ip,session): #任务线程
    global Queue,count,Max_count
    i=0
    cookie=cookiejar.CookieJar()
    while(i<time_max):
        if not (session):
            cookie = cookiejar.CookieJar()

        cookie=visit(url,headers,proxy_ip,cookie)
        if (cookie==False):
            while (True):  # 若队列为空则等待
                try:
                    proxy_ip = Queue.get_ip(block=False)
                    break
                except queue.Empty:
                    pass
                time.sleep(3)
                if (count >= Max_count):
                    return
            count = count + 1
            cookie=cookiejar.CookieJar()

        else:
            i = i + 1
            time.sleep(time_delay)
        if(count>=Max_count):
            return


    Queue.put_ip(proxy_ip)  #使用完放回队列


