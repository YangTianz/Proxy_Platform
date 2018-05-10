# -*- coding: UTF-8 -*-

from urllib import request
from Utils import DBUtils
if __name__ == '__main__' :
    '''
            url="http://localhost/api/?url=http://www.tabao.com&&&time_max=1&&&time_delay=10&&&request_con=1"
            response=request.urlopen(url)
            print(response.read().decode())
'''
    print(DBUtils.showAllIP())
    DBUtils.changeIP_AN(1,'103.109.56.69',8080)