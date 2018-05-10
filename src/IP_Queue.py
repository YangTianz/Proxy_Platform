# -*- coding: UTF-8 -*-

from queue import Queue
import DBUtils

class IP_Queue:#创建可用IP队列

    def __init__(self,size):
        self.__ip_queue=Queue()
        ip_list=DBUtils.getIPs(size)
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