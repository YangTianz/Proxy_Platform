# -*- coding: UTF-8 -*-
from IP import *
import time
import pymysql

#数据库的地址，可以自己去看一下
host = '111.230.249.201'
port = 3306
user = 'test'
passwd = 'Sustech15'
db = 'Proxy_Platform'

#---------------ipPool table-------------------
#输出所有的IP信息
def showAllIP():
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select * from ipPool;"
    cursor.execute(sql)
    print("id\tAddress\tPort\tLocation\tLivingTime\tAnonmyous\tCategory")
    m = cursor.fetchone()
    while (m!=None):
        for i in m:
            print(i, end='\t')
        print()
        m = cursor.fetchone()
    conn.close()

# 输入一个IP的id，返回一个IP类
def getIPInfo(id):
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
def deleteIPinfo(id):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "delete from ipPool where idIP=%d" % id
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 在数据库中新增一条IP信息，需要输入的有 地址、端口
def insertIPinfo(IP):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "insert into ipPool (Address, Port, Location, IsAnon, Categ) values ('%s', %d, '%s', %d, '%s');" \
          % (IP.getAddress(), IP.getPort(), IP.getLocation(), IP.getAnon(), IP.getCategory())
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 清空数据库 ipPool
def resetDatabases():
    op = input("Are you sure?y/n\n")
    if (op=='y'):
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        cursor = conn.cursor()
        sql = "delete from Proxy_Platform.ipPool where idIP !=0;"
        sql += "alter table Proxy_Platform.ipPool auto_increment=1;"
        cursor.execute(sql)
        conn.commit()
        conn.close()

#通过输入IP的信息来获取IP地址，这个功能在后续需要修改ResponeseTime 数据库时会被用到（需要提供ip_id）
def getIPID(Address, Port):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select idIP from Proxy_Platform.ipPool where Address = '%s' and Port = %d;" % (Address, Port)
    cursor.execute(sql)
    m = cursor.fetchone()
    conn.close()
    return m[0]

#---------------Website table-------------------
#输出所有网页信息，包括URL和用户访问的时间
def showAllWeb():
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
def getWebsiteInfo(id):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select * from Websites where idWebsites=%d;" % id
    cursor.execute(sql)
    m = cursor.fetchone()
    conn.close()
    return m

# 生成一个新的Website数据，只需要输入 URL，时间会自动生成
def insertWebsiteInfo(url):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "insert into Websites (URL, Time) values ('%s', '%s');" \
          % (url , time.asctime())
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 删除记录
def deleteWebsiteinfo(id):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "delete from Websites where idWebsites=%d" % id
    cursor.execute(sql)
    conn.commit()
    conn.close()

def resetDatabasesWebsite():
    op = input("Are you sure?y/n\n")
    if ( op == 'y'):
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
def showAllRT():
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

# 生成一条新纪录，记录指定i对指定网站的响应时间，以及返回信息
def genResInfo(URLID, IPID, ResponseTime, Method, StatusCode, Header):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "insert into ResponseTime (URLid, ip_id, ResponseTime, Method, StatusCode, Header) "
    sql += "values (%d, %d, %d, '%s', %d, '%s');" \
        % (URLID, IPID, ResponseTime, Method, StatusCode, Header)
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 根据 网站id 和 ip id 更改响应时间
def updateResTimeByID(URLID, IPID, newtime):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "update ResponseTime set ResponseTime=%d where URLid=%d and ip_id=%d" \
        % (newtime, URLID, IPID)
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 根据 网站id 和 ip id 更改网站返回的信息，包括请求方式、状态吗、返回Header
def updateResValueByID (URLID, IPID, Method, StatusCode, Header):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "update ResponseTime set Method='%s', StatusCode=%d, Header='%s' where URLid=%d and ip_id=%d" \
        % (Method, StatusCode, Header, URLID, IPID)
    cursor.execute(sql)
    conn.commit()
    conn.close()

def deleteByID(URLID, IPID):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "delete from Proxy_Platform.ResponseTime where URLid=%d and ip_id=%d" \
        % (URLID, IPID)
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 输出所有的Response信息
def showAllRes():
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select * from ResponseTime;"
    cursor.execute(sql)
    m = cursor.fetchone()
    print("id\tURLid\tip_id\tResTime\tMethod\tCode\tHeader\t")
    while (m!=None):
        for i in m:
            print(i, end='\t')
        print()
        m = cursor.fetchone()
    conn.close()

# 根据访问的网址获取id
def getidByURL(url):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select idWebsites from Websites where URL = '%s'" % url
    cursor.execute(sql)
    m = cursor.fetchone()
    conn.close()
    return m[0]

def getAvailableIP():
    # 获取可用IP
    # 由于抓取IP还未完成所以直接返回了ip list样例

    return [
        {"https": "58.219.173.18:9797"},
        {"https": "219.79.226.5:9064"},
        {"https": "121.201.33.100:16448"},
        {"https": "14.29.47.90:3128"},
        {"https": "116.19.98.249:9797"},
        {"https": "139.227.252.141:8118"},
        {"https": "183.159.82.123:18118"},
        {"https": "101.27.20.7:61234"},
        {"https": "27.209.165.14:61234"},
        {"https": "182.202.220.23:61234"},
        {"https": "122.72.18.34:80"}
    ]

# 从数据库里随机取10个IP
def getIPs(n):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    list = []
    for i in range(n):
        # sql = "select * from ipPool order by rand() LIMIT %d" Method 1效率太低
        #sql = r"select * from ipPool where idIP>="\  Method 2 not precise
        #    +"((select max(idIP) from ipPool) - 1 - (select min(idIP) from ipPool))* RAND() + (select min(idIP) from ipPool) limit 3"
        sql = """
        select *   
        from ipPool as t1 join (select round(rand() * ((select max(idIP) from ipPool)-(select min(idIP) from ipPool))+(select min(idIP) from ipPool)) as id) as t2   
        where t1.idIP >= t2.id   
        order by t1.idIP limit 1; 
        """
        cursor.execute(sql)
        m = cursor.fetchone()
        a = IP(m[1], m[2])
        a.setLocation(m[3])
        a.setAnon(m[5])
        a.setCategory(m[6])
        list.append(a)

    return list

