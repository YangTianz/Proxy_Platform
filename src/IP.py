# -*- coding: UTF-8 -*-
from DBUtils import *;

class IP:

    #初始化时必须有IP的地址和端口，其他三个属性默认设为空，是否匿名设为-1
    def __init__(self, address, port):
        self.__address = address
        self.__port = port
        self.__isAnon = -1
        self.__location = ""
        self.__categ = ""

    
    def getAddress(self):
        return self.__address

    def getPort(self):
        return self.__port

    # 用于测试IP的匿名、类型，未完成
    def checkIPStatus(self):
        return True


#以下为IP类的三个不必要属性，IP的地理位置、IP的类型（HTTP/HTTPS）、是否匿名
    def setLocation(self, loc):
        self.__location = loc
    
    def getLocation(self):
        return self.__location

    #设置是否匿名，默认为-1，表示未设置，如果是匿名请设为1，透明请设为0
    def setAnon(self, a):
        self.__isAnon = a

    def getAnon(self):
        return self.__isAnon


    def setCategory(self, cat):
        self.__categ = cat

    def getCategory(self):
        return self.__categ
