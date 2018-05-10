# -*- coding: UTF-8 -*-
from Utils.IP import *
import time
import pymysql

host = '111.230.249.201'
port = 3306
user = 'test'
passwd = 'Sustech15'
db = 'Proxy_Platform'

"""   --------------------说明--------------------------
void    showAllIP():
打印数据库 ipPool 中所有的 IP 信息
IP      getIPInfo(id):
输入一个 IP 的 id（int），返回这个 IP 的信息，若 id 不存在，返回 NULL
void    deleteIPinfo(id):
输入一个 IP 的 id（int），删除这一条记录，无返回
void    insertIPinfo(IP):
新增一条 IP 记录，若重复则不添加
int     getIPID(Address, Port):
输入地址（str）、端口（int），获取相应的 IP 的 id

void    showAllWeb():
打印数据库 Websites 中所有的信息
list    getWebsiteInfo(id):
输入 Websites 的 id，获取所有信息
int     insertWebsiteInfo(url):
新增一条 URL 记录， 返回其在数据库中的 id
void    deleteWebsiteinfo(id):
输入一个 URL 的 id（int），删除这一条记录，无返回
int     getidByURL(url):
输入 url（str）信息，获取在 Websites 表中的 id

void    showAllRes():
打印数据库 ResponseTime 中所有的信息
void    genResInfo(URLID, IPID, ResponseTime, Method, StatusCode, Header):
生成一条新的记录，数据类型（int，int，int，str，int，str）
void    updateResTimeByID(URLID, IPID, newtime):
------未定-------
void    updateResValueByID (URLID, IPID, Method, StatusCode, Header):
------未定-------
void    deleteByID(URLID, IPID):
根据 URLid 和 IPid 删除记录

list<IP>getIPs(n):
输入需要获取的 ip 数 n，随机返回 n 个 ip 地址

void    resetDatabases():
清空数据库

"""

# --------------ipPool table-------------------
# 输出所有的IP信息
def showAllIP():
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select * from ipPool;"
    cursor.execute(sql)
    m = cursor.fetchone()
    ip_list=[]
    while (m!=None):
        Address=m[1]
        Port=m[2]
        ip=Address+":"+str(Port)
        ip_list.append(ip)
        m = cursor.fetchone()
    conn.close()
    return ip_list

def showStatus():
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select * from ipPool;"
    cursor.execute(sql)
    m = cursor.fetchone()
    sentence=""
    while (m != None):
        for i in m:
            sentence=sentence+str(i)+"\t"
        sentence=sentence+'\n'
        m = cursor.fetchone()
    conn.close()
    print(sentence)
    return sentence

def changeIP_AN(Anonmyous,Address,Port):
    id = getIPID(Address, int(Port))

    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql="update ipPool set IsAnon='%d' where idIP=%d" % (Anonmyous, id)
    cursor.execute(sql)
    conn.commit()
    conn.close()


# 输入一个IP的id，返回一个IP类
def getIPInfo(id):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select * from ipPool where idIP=%d;" % id
    cursor.execute(sql)
    m = cursor.fetchone()
    conn.close()
    if m!=None:
        a = IP(m[1],m[2])
        a.setLocation(m[3])
        a.setAnon(m[5])
        a.setCategory(m[6])
        return a
    else:
        return

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
    sql = "select * from ipPool where Address='%s' and Port=%d " % (IP.getAddress() , IP.getPort())
    cursor.execute(sql)
    m = cursor.fetchone()
    if m==None:
        sql = "insert into ipPool (Address, Port, Location, IsAnon, Categ) values ('%s', %d, '%s', %d, '%s');" \
              % (IP.getAddress(), IP.getPort(), IP.getLocation(), IP.getAnon(), IP.getCategory())
        cursor.execute(sql)
        conn.commit()
    else:
        pass
    conn.close()


# 通过输入IP的信息来获取IP地址，这个功能在后续需要修改ResponeseTime 数据库时会被用到（需要提供ip_id）
def getIPID(Address, Port):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select idIP from Proxy_Platform.ipPool where Address = '%s' and Port = %d;" % (Address, Port)
    cursor.execute(sql)
    m = cursor.fetchone()
    conn.close()
    return int(m[0])

# -------------------------------------Website table--------------------------------------------
# 输出所有网页信息，包括URL和用户访问的时间
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

# 获取一个网页的信息
def getWebsiteInfo(id):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select * from Websites where idWebsites=%d;" % id
    cursor.execute(sql)
    m = cursor.fetchone()
    conn.close()
    return m

# 生成一个新的Website数据，只需要输入 URL，时间会自动生成 , 随后返回网站id
def insertWebsiteInfo(url):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "insert into Websites (URL, Time) values ('%s', '%s');" \
          % (url , time.asctime())
    cursor.execute(sql)
    conn.commit()
    sql = "select idWebsites from Websites where URL='%s'" % url
    cursor.execute(sql)
    m = cursor.fetchone()
    conn.close()
    return int(m[0])

# 删除记录
def deleteWebsiteinfo(id):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "delete from Websites where idWebsites=%d" % id
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 根据访问的网址获取id
def getidByURL(url):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = "select idWebsites from Websites where URL = '%s'" % url
    cursor.execute(sql)
    m = cursor.fetchone()
    conn.close()
    return int(m[0])

# -----------------------------------ResponseTime----------------------------------------
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

# 根据 网站id 和  更改响应时间
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

# -----------------------------------------------------------------------------

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

# 清空数据库
def resetDatabases():
    op = input("Are you sure?y/n\n")
    if (op=='y'):
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        cursor = conn.cursor()
        sql = "delete from Proxy_Platform.ipPool where idIP !=0;"
        sql += "alter table Proxy_Platform.ipPool auto_increment=1;"
        cursor.execute(sql)
        sql = "delete from Proxy_Platform.Websites where idWebsites !=0;"
        sql += "alter table Proxy_Platform.Websites auto_increment=1;"
        cursor.execute(sql)
        sql = "delete from Proxy_Platform.ResponseTime where idResponseTime!=0;"
        sql += "alter table Proxy_Platform.ResponseTime auto_increment=1;"
        cursor.execute(sql)
        conn.commit()
        conn.close()

