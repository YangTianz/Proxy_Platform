# -*- coding: UTF-8 -*-
import time
import re
import json
import threading
from IP_Queue import *
from http import cookiejar
import queue
from Visit_Main import visit
from queue import Queue



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

        ipQueue = IP_Queue(Max_count[0])  # 初始化可用ip队列

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


        Result_list.append("No error")


        for i in range(request_con):

            while (True):
                try:
                    proxy_ip = ipQueue.get_ip(block = False)  # 从可用ip队列中取出首ip,取出失败则将sleep几秒
                    break
                except queue.Empty:
                    pass
                time.sleep(3)   #取出IP失败
                if (count[0] >= Max_count[0]):
                    Result_list=["超出出错次数"]
                    return None
            t = threading.Thread(target=Visit_Thread, args=(i+1,url, headers, method,time_max, time_delay, proxy_ip,cookie,timeout,session,data))
            t.start()

        Thread_count=request_con
        waittime = time.time()
        while(True):

            try:
                Failed_Thread.get(block=False)
                Thread_count=Thread_count+1
                while (True):
                    try:
                        proxy_ip = ipQueue.get_ip(block=False)  # 从可用ip队列中取出首ip,取出失败则将sleep几秒
                        break
                    except queue.Empty:
                        pass
                    time.sleep(3)  # 取出IP失败
                t = threading.Thread(target=Visit_Thread,
                                     args=(Thread_count, url, headers,method, time_max, time_delay, proxy_ip,cookie, timeout,session,data))
                t.start()
            except queue.Empty:
                if(time.time()-waittime>=60):
                    print("I'm alive _(:з」∠)_")
                    waittime=time.time()
                time.sleep(10)
            if(Finish_count[0] >= request_con):
                break

        if(count[0]>=Max_count[0]):
            Result_list=["超出出错次数"]
            return None


    def get_result(self):
        global Result_list
        return Result_list
    def get_session(self):
        global Session
        return Session




def Visit_Thread(index,url,headers,method,time_max,time_delay,proxy_ip,cookie,timeout,session,data): #任务线程
    global count,Max_count,Finish_count,Result_list,Failed_Thread,mutex
    i=0
    Wrong = 0
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

            mutex.acquire()
            if(session):
                return_result={
                    "ip":proxy_ip,
                    "response":result
                }
                Result_list.append(return_result)
            else:
                return_result={
                    "response":result
                }
                Result_list.append(return_result)
            mutex.release()

            if(i==time_max):
                mutex.acquire()
                Finish_count[0]=Finish_count[0]+1
                mutex.release()
                return
            time.sleep(time_delay)
        if(count[0]>=Max_count[0]) and i<time_max:
            print("thread" + str(index)+ " failed!")
            return





