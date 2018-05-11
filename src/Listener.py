## -*- coding: utf-8 -*-

from flask import Flask, request
from Schedule.Scheduler import *
from  proxy_spider.proxyspider import run_spider
from Valid_check import Checker



app=Flask(__name__)

@app.route('/api/')
def listener():
    url = request.args.get('url')
    try:
        url=request.args.get('url')
    except:
        return "No url!"
    try:
        time_max=int(request.args.get('time_max'))
    except:
        time_max=""
    try:
        headers = request.args.get('headers')
    except:
        headers=""
    try:
        method=request.args.get('get')
    except:
        method =""
    try:
        data=request.args.get('data')
    except:
        data=""
    try:
        time_delay=float(request.args.get('time_delay'))
    except Exception as e:
        time_delay=""
    try:
        request_con=int(request.args.get('request_con'))
    except:
        request_con=""
    try:
        session=request.args.get('session')
        if(session=="True"):
            session=True
        elif(session=="False"):
            session=False
    except:
        session=""
    try:
        cookies=request.args.get('cookies')
    except:
        cookies=""
    try:
        timeout=request.args.get('timeout')
    except:
        timeout=""
    url = request.args.get('url')
    time_max = int(request.args.get('time_max'))
    headers = None
    data = None
    session = request.args.get('session')
    cookies = None
    timeout = None
    Method="get"
    time_delay=20
    request_con = int(request.args.get('request_con'))


    result=get_result(url,headers,method,data,time_max,time_delay,request_con,session,timeout,cookies)
    return result

@app.route('/status')
def status():
    return DBUtils.showStatus()

def get_result(url,headers,method,data,time_max,time_delay,request_con,session,timeout,cookie):
    if(headers==None):
        headers={'User-agent':'Mozilla/5.0'}
    if(method==None):
        method="get"
    if(data==None):
        data=None
    if(time_max==None):
        time_max=1
    if(time_delay==None):
        time_delay=1
    if(request_con==None):
        request_con=1
    if(session==None):
        session=False
    if(timeout==None):
        timeout=20
    if(cookie==None):
        cookie=cookiejar.CookieJar()


    result = Scheduler(url,headers,method,data,time_max,time_delay,request_con,session,timeout,cookie)
    result_list = result.get_result()
    if(len(result_list)==1):
        return result_list[0]

    session = result.get_session()
    if (session):
        ip_list = "["
        response_list = "{[[[[["
        number = 0
        for i in result_list:
            if(number==0):
                number=number+1
                continue
            if (number < len(result_list) - 1):
                ip_list = ip_list + str(i['ip']) + ','
                response_list = response_list + i['response'] + "]]]]],[[[[["
            else:
                ip_list = ip_list + str(i['ip'])
                response_list = response_list + i['response']
            number = number + 1

        ip_list = ip_list + ']'
        response_list = response_list + "]]]]]}"
        Result = {"ip": ip_list, "response": response_list}
    else:
        response_list = "{[[[[["
        number = 0
        for i in result_list:
            if (number == 0):
                number = number + 1
                continue
            if (number < len(result_list) - 1):
                response_list = response_list + i['response'] + "]]]]],[[[[["
            else:
                response_list = response_list + i['response']
            number = number + 1
        response_list = response_list + "]]]]]}"
        Result = {"response": response_list}
    return json.dumps(Result)





if __name__ == '__main__':
    run_spider()  # 启动爬虫爬可用IP
    app.run(host='0.0.0.0', port=80, debug=True)


