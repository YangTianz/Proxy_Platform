# -*- coding: UTF-8 -*-

from Scheduler import *


if __name__ == '__main__' :
   result=Scheduler("http://www.baidu.com",time_max=1,time_delay=2,request_con=1,session=True) #访问的方法
   #参数为： URL 网址， time_max 为 每个ip最大访问量 ， time_delay 为 每次访问间隔 ， request_con 为 任务并发数 ， session 为 Session功能
   result_list = result.get_result()
   session=result.get_session()
   if(session):
      ip_list="["
      response_list="{[[[[["
      number=0
      for i in result_list:
         if (number == 0):
            number = number + 1
            continue
         if(number<len(result_list)-1):
            ip_list=ip_list+str(i['ip'])+','
            response_list=response_list+i['response']+"]]]]],[[[[["
         else:
            ip_list = ip_list + str(i['ip'])
            response_list = response_list + i['response']
         number=number+1
      ip_list=ip_list+']'
      response_list = response_list + "]]]]]}"
      Result={"ip":ip_list,"response":response_list}
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



