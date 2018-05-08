#coding=utf-8
import time
import re
import threading
from IP_Queue import *
from http import cookiejar
import queue
from Visit_Main import visit
from queue import Queue



class Scheduler:

    def __init__(self,url,headers={'User-agent':'Mozilla/5.0'},time_max=1,time_delay=1,request_con=1,session=False):#任务调度
        # url 为访问的地址， headers 为报头， time_max 为每个ip最大访问数， time_delay 为访问间隔, request_con 为任务并发数

        global ipQueue, count, Max_count, mutex, Finish_count, Result_list, Failed_Thread

        mutex = threading.Lock()  # 计数锁
        ipQueue = IP_Queue()  # 初始化可用ip队列
        Failed_Thread = Queue()
        count = [0] # 初始化报错导致切换新ip的计数。连续访问失败三次将会切换新ip
        Finish_count = [0]
        Max_count = [request_con * time_max]
        Result_list = []

        if(request_con<5):
            Max_count[0]=5 * time_max     #初始化报错最大值

        if not re.match(r'^https?:/{2}\w.+$', url):  # 若url不合法则返回error
            print("error")
            return


        for i in range(request_con):

            while (True):
                try:
                    proxy_ip = ipQueue.get_ip(block = False)  # 从可用ip队列中取出首ip,取出失败则将sleep几秒
                    break
                except queue.Empty:
                    pass
                time.sleep(3)   #取出IP失败
                if (count[0] >= Max_count[0]):
                    print("shit!")
                    return
            t = threading.Thread(target=Visit_Thread, args=(i+1,url, headers, time_max, time_delay, proxy_ip, session))
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
                                     args=(Thread_count, url, headers, time_max, time_delay, proxy_ip, session))
                t.start()
            except queue.Empty:
                if(time.time()-waittime>=60):
                    print("I'm alive _(:з」∠)_")
                    waittime=time.time()
                time.sleep(10)
            if(Finish_count[0] >= request_con):
                break



        if(count[0]>=Max_count[0]):
            print("shit!")
        for i in Result_list:
            print(i)




def Visit_Thread(index,url,headers,time_max,time_delay,proxy_ip,session): #任务线程
    global count,Max_count,Finish_count,Result_list,Failed_Thread
    i=0
    Wrong = 0
    result=cookiejar.CookieJar()

    while(i<time_max):
        if not (session):
            cookie = cookiejar.CookieJar()
        else:
            if not (len(result)==2):
                cookie = result
            else:
                cookie = result[0]

        result=visit(url,headers,proxy_ip,cookie)

        if (result==False):
            Wrong=Wrong+1
            if (Wrong == 3):
                count[0] = count[0] + 1
                Failed_Thread.put(1)
                print("thread " + str(index) + " failed!")
                return
            result=cookiejar.CookieJar()

        else:
            Wrong = 0
            i = i + 1
            Result_list.append(result[1])
            if(i==time_max):
                Finish_count[0]=Finish_count[0]+1
                return
            time.sleep(time_delay)
        if(count[0]>=Max_count[0]) and i<time_max:
            print("thread" + str(index)+ " failed!")
            return





