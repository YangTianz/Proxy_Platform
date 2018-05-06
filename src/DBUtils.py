# -*- coding: UTF-8 -*-
import pymysql
from IP import *
import sys

#数据库的地址，可以自己去看一下
host = '111.230.249.201'
port = 3306
user = 'root'
passwd = 'Sustech15'
db = 'Proxy_Platform'

#---------------ipPool table-------------------
#输出所有的IP信息
def ShowAllIP():
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select * from ipPool;"
    cursor.execute(sql)
    m = cursor.fetchone()
    while (m!=None):
        for i in m:
            print(i, end='  ')
        print()
        m = cursor.fetchone()
    conn.close()

# 输入一个IP的id，返回一个IP类
def GetIPInfo(id):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select * from ipPool where idIP=%d;" % id
    cursor.execute(sql)
    m = cursor.fetchone()
    print(m)
    conn.close()
    a = IP(m[1],m[2])
    a.setLocation(m[3])
    a.setAnon(m[5])
    a.setCategory(m[6])
    return a

# 输入一个IP的id，在数据库中删除这个IP的信息
def DeleteIPinfo(id):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "delete from ipPool where idIP=%d" % id
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 在数据库中新增一条IP信息，需要输入的有 地址、端口
def InsertIPinfo(IP):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "insert into ipPool (Address, Port, Location, IsAnon, Categ) values ('%s', %d, '%s', %d, '%s');" \
          % (IP.getAddress(), IP.getPort(), IP.getLocation(), IP.getAnon(), IP.getCategory())
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 清空数据库 ipPool
def ResetDatabases():
    op = input("Are you sure?y/n\n")
    if (op=='y'):
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        cursor = conn.cursor()
        sql = "delete from Proxy_Platform.ipPool where idIP !=0;"
        sql += "alter table Proxy_Platform.ipPool auto_increment=1;"
        cursor.execute(sql)
        conn.commit()
        conn.close()

#---------------Website table-------------------
#输出所有网页信息，包括URL和用户访问的时间
def ShowAllWeb():
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select * from Websites;"
    cursor.execute(sql)
    m = cursor.fetchone()
    while (m!=None):
        for i in m:
            print(i, end='  ')
        print()
        m = cursor.fetchone()
    conn.close()

#获取一个网页的信息
def GetWebsiteInfo(id):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select * from Websites where idWebsites=%d;" % id
    cursor.execute(sql)
    m = cursor.fetchone()
    conn.close()
    return m

#生成一个新的Website数据，需要输入 URL 和 当前时间   time.asctime()
def InsertWebsiteInfo(url, time):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "insert into Websites (URL, Time) values ('%s', '%s');" \
          % (url , time)
    cursor.execute(sql)
    conn.commit()
    conn.close()

#删除记录
def DeleteWebsiteinfo(id):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "delete from Websites where idWebsites=%d" % id
    cursor.execute(sql)
    conn.commit()
    conn.close()

def ResetDatabasesWebsite():
    op = input("Are you sure?y/n\n")
    if (op=='y'):
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        cursor = conn.cursor()
        sql = "delete from Proxy_Platform.Websites where idWebsites !=0;"
        sql += "alter table Proxy_Platform.Websites auto_increment=1;"
        cursor.execute(sql)
        conn.commit()
        conn.close()

#---------------ResponseTime
#idResponseTime URLid ip_id ResponseTime Method StatusCode Header
#输出所有的IP信息
def ShowAllRT():
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select * from ResponseTime;"
    cursor.execute(sql)
    m = cursor.fetchone()
    while (m!=None):
        for i in m:
            print(i, end='  ')
        print()
        m = cursor.fetchone()
    conn.close()

def InsertA():
    pass
