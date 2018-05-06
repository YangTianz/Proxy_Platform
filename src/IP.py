from DBUtils import *;

class IP:

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

    def setLocation(self, loc):
        self.__location = loc

    def setAnon(self, a):
        self.__isAnon = a

    def setCategory(self, cat):
        self.__categ = cat

    def getLocation(self):
        return self.__location

    def getAnon(self):
        return self.__isAnon

    def getCategory(self):
        return self.__categ
