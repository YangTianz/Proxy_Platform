# -*- coding: UTF-8 -*-

class IP:

    #初始化时必须有IP的地址和端口，其他三个属性默认设为空，是否匿名设为-1
    def __init__(self, address, port):
        self.__address = address
        self.__port = port
        self.__isAnon = -1
        self.__location = ""
        self.__categ = "HTTP"

    def get(self):
        re = self.__address
        re += ':'
        re += str(self.__port)
        re += ':'
        re += self.getCategory()
        return re  # 11.11.11.11:80:HTTP

    def getAddress(self):
        return self.__address

    def getPort(self):
        return self.__port

    # 显示IP的信息
    def show(self):
        mes = "IP Address: %s, Port: %d" % (self.__address, self.__port)
        if self.__location!="":
            mes += ", Location: %s" % self.__location
        if self.__isAnon!=-1:
            mes += ", isAnonmyous: %s" % (self.__isAnon==1)
        if self.__categ != "":
            mes += ", Category: %s" % self.__categ
        print(mes)

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
        if cat!='HTTP' and cat!='HTTPS':
            self.__categ = 'HTTP'
        else:
            self.__categ = cat

    def getCategory(self):
        return self.__categ
