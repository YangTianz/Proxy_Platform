
from flask import Flask, request as request1
from Schedule.Scheduler import *
from  proxy_spider.proxyspider import run_spider
from Utils import DBUtils
from Utils import redisdb



app=Flask(__name__)

@app.route('/api/')
def listener():
    url = request1.args.get('url',None)
    time_max=int(request1.args.get('time_max',1))
    headers = request1.args.get('headers','{"User-agent":"Mozilla/5.0"}')
    method=request1.args.get('method','get')
    data=request1.args.get('data',None)
    time_delay=float(request1.args.get('time_delay',1))
    request_con=int(request1.args.get('request_con',1))
    session=request1.args.get('session',False)
    if(session=="True"):
        session=True
    elif(session=="False"):
        session=False
    cookies=request1.args.get('cookies',None)
    timeout=request1.args.get('timeout',20)
    try:
        headers=json.loads(headers)
    except:
        return "data load error"

    result=get_result(url,headers,method,data,time_max,time_delay,request_con,session,timeout,cookies)
    return result

@app.route('/status')
def status():
    r=redisdb.RedisClient()
    return r.ipstatus()

def get_result(url,headers,method,data,time_max,time_delay,request_con,session,timeout,cookie):

    if(cookie==None):
        cookie=cookiejar.CookieJar()


    result = Scheduler(url,headers,method,data,time_max,time_delay,request_con,session,timeout,cookie)
    result_list = result.get_result()
    if(len(result_list)==1):
        result={"error":result_list[0]}
        return json.dumps(result)

    session = result.get_session()
    if(session==1):
        session=DBUtils2.addSession(result_list['ip'])
    if (session):
        response_list = []
        number = 0
        for i in result_list:
            if(number==0):
                number=number+1
                continue
            else:
                response_list.append(i['response'])
            number = number + 1

        Result = {"response": response_list,"session":session}
    else:
        response_list = []
        number = 0
        for i in result_list:
            if (number == 0):
                number = number + 1
                continue
            response_list.append(i['response'])
            number = number + 1
        Result = {"response": response_list}
    return json.dumps(Result)





if __name__ == '__main__':
    #run_spider()  # 启动爬虫爬可用IP
    app.run(host='0.0.0.0', port=8000,debug=True)


