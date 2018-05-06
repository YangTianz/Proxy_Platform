#coding=utf-8
import time
import re
import threading
from urllib import request,parse


#import database


def visit(url,headers,proxy_ip):#访问网站
    response_time=-1
    try:


        httpproxy_handler = request.ProxyHandler(proxy_ip)
        opener = request.build_opener(httpproxy_handler)


        Request = request.Request(url)
        for key in headers.keys():
            Request.add_header(key,headers[key])    #添加报文

        response_time = time.time()
        response = opener.open(Request) #访问过程
        response_time = time.time() - response_time #响应时间

    except TimeoutError:
        response_time=-1
    print(response.read())
    #return_result(response.read())


def get_ip(url,num): #获取
    url=parse.urlparse(url=url) #解析url
    url=url.netloc  #将域名取出来。例如http://www.baidu.com/asdasdasd 取出www.baidu.com

    proxy = [
        {"https": "58.219.173.18:9797"},
        {"https": "219.79.226.5:9064"},
        {"https": "121.201.33.100:16448"},
        {"https": "14.29.47.90:3128"},
        {"https": "116.19.98.249:9797"}
    ]

    proxy_list=[]
    for i in range(num):
        proxy_list.append(proxy[4-i])

    #实际项目中应从数据库中取出num个合适的ip
    #proxy_list=database.get_ip(url,num)

    return proxy_list


def Visit_Thread(url,headers,time_max,time_delay,proxy_ip): #任务线程
    for i in range(time_max):
        visit(url,headers,proxy_ip)
        time.sleep(time_delay)

def scheduler(url,headers={'User-agent':'Mozilla/5.0'},time_max=1,time_delay=1,request_con=1):  #任务调度
    #url 为访问的地址， headers 为报头， time_max 为每个ip最大访问数， time_delay 为访问间隔, request_con 为任务并发数

    if not re.match(r'^https?:/{2}\w.+$', url): #若url不合法则返回error
        print("error")

    proxy_list=get_ip(url,request_con) #获取适合ip
    for i in range(request_con):
        proxy_ip=proxy_list[i]
        t=threading.Thread(target=Visit_Thread,args=(url,headers,time_max,time_delay,proxy_ip,))
        t.start()

if __name__ =='__main__':
    scheduler("http://www.baidu.com",request_con=2,time_delay=2,time_max=3)