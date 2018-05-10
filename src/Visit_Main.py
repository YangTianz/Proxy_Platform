# -*- coding: UTF-8 -*-

from http import cookiejar
from urllib import request,error,parse
import time
import socket


def visit(url,headers,proxy_ip,cookie=cookiejar.CookieJar(),timeout=20,method="get",data=None):#单次访问网站
    socket.setdefaulttimeout(timeout)
    for key in proxy_ip:
        ip = proxy_ip[key]
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


    except error.URLError as e:
        sentence = time.asctime(time.localtime(time.time())) + " use " + ip + " requested " + url + " failed. "
        print(sentence+"\n"+ str(e.reason))
        return False
    sentence = time.asctime(time.localtime(time.time())) + " use " + ip + " requested " + Response.geturl() + \
               " success. Status:" + status +". Old url: "+url
    print(sentence)
    return Response.read().decode()