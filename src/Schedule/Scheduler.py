# -*- coding: UTF-8 -*-
import time
import re
import json
import threading
from Schedule.IP_Queue import *
import queue
from queue import Queue
from http import cookiejar
from urllib import request,error,parse
import time
import socket
from Utils import DBUtils2
class Scheduler:

    def __init__(self,url,headers={'User-agent':'Mozilla/5.0'},method="get",data=None,time_max=1,time_delay=1,request_con=1,
                 session=False,timeout=20,cookie=cookiejar.CookieJar()):#任务调度
        # url 为访问的地址， headers 为报头， time_max 为每个ip最大访问数， time_delay 为访问间隔, request_con 为任务并发数,
        #  session为连续ip访问功能，将返回使用的ip和cookies和访问数据

        global ipQueue, count, Max_count, mutex, Finish_count, Result_list, Failed_Thread,Session

        mutex = threading.Lock()  # 计数锁

        Failed_Thread = Queue()
        count = [0] # 初始化报错导致切换新ip的计数。连续访问失败三次将会切换新ip
        Finish_count = [0]
        Max_count = [request_con * time_max]
        Result_list = []
        Session=session


        if(request_con<5):
            Max_count[0]=5 * time_max     #初始化报错最大值

        ipQueue = IP_Queue(Max_count[0],session)  # 初始化可用ip队列
        if(ipQueue.checkip()==None):
            Result_list.append("session编号错误")
            return None

        if not re.match(r'^https?:/{2}\w.+$', url):  # 若url不合法则返回error
            print("error")
            Result_list.append("url格式错误")
            return None
        if(data!=None):
            try:
                json.loads(data)
            except ValueError:
                Result_list.append("data的JSON格式错误")
                return None
        if(session!=False) and (request_con!=1):
            Result_list.append("session功能时request_con为1")
            return None

        #DBUtils.insertWebsiteInfo(getURL(url))
        Result_list.append("No error")



        Thread_count=1
        while(Thread_count<=request_con):
            proxy_ip = ipQueue.get_ip(block = False)
            t = threading.Thread(target=Visit_Thread, args=(Thread_count,url, headers, method,time_max, time_delay, proxy_ip,cookie,timeout,data))
            t.start()
            Thread_count+=1

        waittime = time.time()
        while(True):

            if(Failed_Thread.qsize()!=0):
                Failed_Thread.get(block=False)
                try:
                    proxy_ip = ipQueue.get_ip(block=False)
                    break
                except queue.Empty:
                    Result_list=["URL Failed"]
                    if(session!=False) or (session!=1):
                        Result_list = ["This session ip fail to request"]
                    return None
                t = threading.Thread(target=Visit_Thread,
                                     args=(Thread_count, url, headers,method, time_max, time_delay, proxy_ip,cookie, timeout,data))
                t.start()
                Thread_count += 1
            else:
                if(time.time()-waittime>=60):
                    print("I'm alive _(:з」∠)_")
                    waittime=time.time()
                time.sleep(5)
            if(Finish_count[0] >= request_con):
                break



    def get_result(self):
        global Result_list
        return Result_list
    def get_session(self):
        global Session
        return Session




def Visit_Thread(index,url,headers,method,time_max,time_delay,proxy_ip,cookie,timeout,data): #任务线程
    global count,Max_count,Finish_count,Result_list,Failed_Thread,mutex,Session,ipQueue
    i=0
    Wrong = 0
    myresult=[]
    while(i<time_max):
        result=visit(url,headers,proxy_ip,cookie,timeout,method,data)
        if (result==False):
            Wrong=Wrong+1
            if (Wrong == 3):
                mutex.acquire()
                count[0] = count[0] + 1
                Failed_Thread.put(1)
                mutex.release()
                print("thread " + str(index) + " failed!")
                return

        else:
            Wrong = 0
            i = i + 1
            myresult.append(result)

            if(i==time_max):
                mutex.acquire()
                Finish_count[0]=Finish_count[0]+1
                mydict={}
                mydict['response']=myresult
                if(Session!=False):
                    mydict['session']=Session
                if(Session==1):
                    mydict['ip']=(ipQueue.checkip()).get()
                Result_list.append(mydict)
                mutex.release()
                return
            time.sleep(time_delay)
        if(count[0]>=Max_count[0]) and i<time_max:
            print("thread" + str(index)+ " failed!")
            return


def visit(url,headers,proxy_ip,cookie=cookiejar.CookieJar(),timeout=20,method="get",data=None):#单次访问网站
    socket.setdefaulttimeout(timeout)
    for key in proxy_ip:
        ip = proxy_ip[key]
        array=ip.split(":")
    try:
        proxy_handler = request.ProxyHandler(proxy_ip)  #创建代理处理器
        cookie_handler = request.HTTPCookieProcessor(cookie)    #创建cookie处理器

        opener = request.build_opener(proxy_handler,cookie_handler)     #创建opener

        if(method=="get"):
            if(data==None):
                RequestA = request.Request(url)
            else:
                data=parse.urlencode(data)
        elif(method=="post"):
            if(data==None):
                RequestA = request.Request(url)
            else:
                RequestA = request.Request(url,data=data)

        for key in headers.keys():
            RequestA.add_header(key,headers[key])    #添加报文头部

        response_time = time.time()
        Response = opener.open(RequestA) #访问
        response_time = time.time() - response_time #响应时间
        status = str(Response.code)  #状态码
        response_header = Response.info()   #返回header

        DBUtils2.insertWebsiteInfo(ip,getURL(url),method,int(status),response_header)


    except error.URLError as e:
        sentence = time.asctime(time.localtime(time.time())) + " use " + ip + " requested " + url + " failed. "
        print(sentence+"\n"+ str(e.reason))
        return False
    sentence = time.asctime(time.localtime(time.time())) + " use " + ip + " requested " + Response.geturl() + \
               " success. Status:" + status +". Old url: "+url
    print(sentence)
    Response=Response.read().decode()
    return Response


def getURL(url):
    headurl = parse.urlparse(url).scheme
    newurl = parse.urlparse(url).netloc
    url = headurl + "://" + newurl
    return url

#a = re.findall(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d*",s)