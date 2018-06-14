import requests, socket
import time
import gevent
from gevent import monkey;monkey.patch_all()
from Utils.redisdb import RedisClient
from Valid_check.Headers import *

requests.adapters.DEFAULT_RETRIES = 5       #设置最大重连次数
socket.setdefaulttimeout(20)        #设置默认超时时间

# 验证网站列表
verifyWeb = ["http://httpbin.org/ip",
             "https://weibo.com",
             "https://www.zhihu.com",
             "https://www.douban.com",
             "https://stackoverflow.com"]

sus = 0    # 记录每次操作可用

"""
可用性验证函数
IP：str，需要验证的IP，格式为"IP:port"
web：str，目标验证网站，格式为"http/https://xxx.xxxx.xxx"
ips：IP实例，来自Utils.IP的class IP，进行增减分数操作对象
IPct：RedisClient实例，来自Utils.redisdb的class RedisClient，包含增减分数操作函数
"""
def validIP(IP,web,ips,IPct):

    '''检查IP可用性'''

    # 设置代理信息
    proxies = {
        'http': IP,
        'https': IP,
    }

    '''开始校验'''
    try:

        if web == "https://www.zhihu.com":
            r = requests.get(web, proxies=proxies, headers=zhihu, timeout=(10, 5))      # 知乎需要header，否则一个也过不了
        else:
            r = requests.get(web, proxies=proxies, timeout=(10, 5))         # 一般情况

        if r.status_code == 200:

            back = r.elapsed.seconds        # 响应时间
            if back < 1:
                IPct.increase(ips, 4)

            elif 1 <= back < 3:
                IPct.increase(ips, 3)

            elif 3 <= back < 5:
                IPct.increase(ips, 2)

            elif 5 <= back < 7:
                IPct.increase(ips, 1)

            global sus
            sus = sus + 1

        else:
            IPct.decrease(ips, 1)

    except:
        IPct.decrease(ips, 1)


if __name__ == "__main__":

    IPct = RedisClient()
    num = IPct.count()        # 库中IP数量
    ip = IPct.batch(0, num)    # 获取数量
    js = []

    """
    持续进行验证，保证IP可用性
    使用gevent，内置事件驱动的异步
    """
    while 1:
        for web in verifyWeb:
            for ips in ip:
                IP = ips.getAddress() + ":" + str(ips.getPort())
                t = gevent.spawn(validIP, IP, web, ips, IPct)
                js.append(t)

            gevent.joinall(js)
            print("当前验证网站可用数量为：%s" % sus)
            sus = 0
            time.sleep(10)

        time.sleep(30)
