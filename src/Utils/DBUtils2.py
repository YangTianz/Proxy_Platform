# -*- coding: UTF-8 -*-
from Utils.IP import *
import time
import pymysql
from Utils.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB


def insertWebsiteInfo(ip,url,method,statuscode,header):
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)
    cursor = conn.cursor()
    sql = "insert into Saves (ip, url, method, statuscode, header) values ('%s', '%s', '%s', '%d' ,'%s');" \
          % (ip,url,method,statuscode,header)
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
