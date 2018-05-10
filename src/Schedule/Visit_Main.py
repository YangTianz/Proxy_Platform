# -*- coding: UTF-8 -*-

from http import cookiejar
from urllib import request,error,parse
import time
import socket
import DBUtils


def visit(url,headers,proxy_ip,cookie=cookiejar.CookieJar(),timeout=20,method="get",data=None):#单次访问网站
    socket.setdefaulttimeout(timeout)
    for key in proxy_ip:
        ip = proxy_ip[key]
        array=ip.split(":")
        address=array[0]
        port=int(array[1])
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
        webid=int(DBUtils.getidByURL(getURL(url)) )  #返回网址id
        ipid=int(DBUtils.getIPID(address,port))  #返回ip id

        DBUtils.genResInfo(webid,ipid,int(response_time),method,int(status),response_header)



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