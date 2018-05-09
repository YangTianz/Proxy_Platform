# -*- coding: UTF-8 -*-

from Scheduler import *


if __name__ == '__main__' :
   Scheduler("https://www.baidu.com",time_max=3,time_delay=2,request_con=5,session=True) #访问的方法
   #参数为： URL 网址， time_max 为 每个ip最大访问量 ， time_delay 为 每次访问间隔 ， request_con 为 任务并发数 ， session 为 Session功能
