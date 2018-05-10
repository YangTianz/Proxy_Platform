## -*- coding: utf-8 -*-

from flask import Flask, request
from Scheduler import *

app=Flask(__name__)

@app.route('/api/')
def listener():
    url=request.args.get('url')
    time_max=""
    headers=""
    method=""
    data=""
    time_delay=""
    request_con=2
    session=True
    cookie=""
    timeout=""

    result=get_result(url,headers,method,data,time_max,time_delay,request_con,session,timeout,cookie)
    return result



def get_result(url,headers,method,data,time_max,time_delay,request_con,session,timeout,cookie):
    if(headers==""):
        headers={'User-agent':'Mozilla/5.0'}
    if(method==""):
        method="get"
    if(data==""):
        data=None
    if(time_max==""):
        time_max=1
    if(time_delay==""):
        time_delay=1
    if(request_con==""):
        request_con=1
    if(session==""):
        session=False
    if(timeout==""):
        timeout=20
    if(cookie==""):
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
    app.run(host='0.0.0.0',port=80,debug=True)
