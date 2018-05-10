# -*- coding: UTF-8 -*-

from Scheduler import *
from urllib import parse
import DBUtils
from urllib import request,error,parse
if __name__ == '__main__' :
            url="http://localhost/api/?url=https://www.baidu.com&&&time_max=1&&&time_delay=10&&&request_con=1"
            response=request.urlopen(url)
            print(response.read())

