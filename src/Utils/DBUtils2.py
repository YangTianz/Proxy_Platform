# -*- coding: UTF-8 -*-
from Utils.IP import *
import time
import pymysql
import random, string
from Utils.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB


def insertWebsiteInfo(ip,url,method,statuscode,header):
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)
    cursor = conn.cursor()
    sql = "insert into Saves (ip, url, method, statuscode, header, time) values ('%s', '%s', '%s', '%d' ,'%s','%s');" \
          % (ip,url,method,statuscode,header,time.asctime())
    cursor.execute(sql)
    conn.commit()
    return

def getByip(ip):
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)
    cursor = conn.cursor()
    sql = "select * from Saves where ip = '%s';" % (ip)
    cursor.execute(sql)
    m = cursor.fetchone()
    print("id\tURLid\tip_id\tResTime\tMethod\tCode\tHeader\t")
    while (m != None):
        for i in m:
            print(i, end='\t')
        print()
        m = cursor.fetchone()
    conn.close()

def getByurl(url):
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)
    cursor = conn.cursor()
    sql = "select * from Saves where url = '%s';" % (url)
    cursor.execute(sql)
    m = cursor.fetchone()
    print("id\tURLid\tip_id\tResTime\tMethod\tCode\tHeader\t")
    while (m != None):
        for i in m:
            print(i, end='\t')
        print()
        m = cursor.fetchone()
    conn.close()

def getAllRes():
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)
    cursor = conn.cursor()
    sql = "select * from Saves;"
    cursor.execute(sql)
    m = cursor.fetchone()
    print("id\tURLid\tip_id\tResTime\tMethod\tCode\tHeader\t")
    while (m!=None):
        for i in m:
            print(i, end='\t')
        print()
        m = cursor.fetchone()
    conn.close()

#-------------------Sessions-----------------------
def addSession(ip):
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)
    cursor = conn.cursor()
    name = name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    sql = "insert into Session (ip, name) values ('%s', '%s');" \
          % (ip, name)
    cursor.execute(sql)
    conn.commit()
    return name;

def getIP(name):
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)
    cursor = conn.cursor()
    sql = "select ip from Session where name='%s';" % name
    cursor.execute(sql)
    m = cursor.fetchone()
    conn.close()
    m = m[0]
    if m != None:
        m = str.split(m,':')
        a = IP(m[0], int(m[1]))
        return a
    else:
        return

def resetDatabases():
    op = input("Are you sure?y/n\n")
    if (op=='y'):
        conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)
        cursor = conn.cursor()
        sql = "delete from Proxy_Platform.Saves where idSaves !=0;"
        sql += "alter table Proxy_Platform.Saves auto_increment=1;"
        cursor.execute(sql)
        conn.commit()
        conn.close()


