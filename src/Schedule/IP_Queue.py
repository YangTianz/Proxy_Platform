# -*- coding: UTF-8 -*-

from queue import Queue
from Utils import redisdb
from Utils import DBUtils2


class IP_Queue:#创建可用IP队列

    def __init__(self,size,session):
        self.__ip_queue=Queue()
        self.__myip=1
        if(session!=False) and (session!=True):
            self.__myip=DBUtils2.getIP(session)
            if(self.__myip==None):
                self.__myip="?"
            self.__ip_queue.put(self.__myip)
            return

        conn = redisdb.RedisClient()
        ip_list= conn.random(size)
        for ip in ip_list:
            address=ip.getAddress()
            port=ip.getPort()
            cat=ip.getCategory()
            ip_port=str(address)+":"+str(port)
            format={cat:ip_port}
            self.__ip_queue.put(format)


    def get_ip(self,block=True):
        return self.__ip_queue.get(block=block)

    def put_ip(self,ip):
        self.__ip_queue.put(ip)

    def empty(self):
        return self.__ip_queue.empty()

    def size(self):
        return self.__ip_queue.qsize()
    def checkip(self):
        if (self.__myip == "?"):
            return None
        return self.__myip
