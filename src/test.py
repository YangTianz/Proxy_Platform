# -*- coding: UTF-8 -*-

from urllib import request
if __name__ == '__main__' :

            url="http://localhost/api/?url=http://www.baidu.com&&&time_max=2&&&time_delay=2&&&request_con=2"
            url="http://localhost/status"
            response=request.urlopen(url)
            print(response.read().decode())
