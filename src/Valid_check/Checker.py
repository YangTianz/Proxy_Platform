import requests, socket
import time
import gevent
from gevent import monkey;monkey.patch_all()
from Utils.redisdb import RedisClient

requests.adapters.DEFAULT_RETRIES = 5       #设置最大重连次数
socket.setdefaulttimeout(20)        #设置默认超时时间

# 验证网站列表
verifyWeb = ["http://httpbin.org/ip",
             "https://weibo.com",
             "https://www.zhihu.com",
             "https://www.douban.com",
             "https://stackoverflow.com"]


headers = {
    "Host": "www.douban.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5478.400 QQBrowser/10.1.1550.400",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"

}
sus = 0

# 可用性验证
def validIP(IP,web,ips,test):

    '''检查IP可用性'''

    # 设置代理信息
    proxies = {
        'http': IP,
        'https': IP,
    }

    '''一次基础校验'''
    try:
        #print("开始验证")
        r = requests.get(web, proxies=proxies, timeout=(10, 10))      #设置超时
        if r.status_code == 200:

            print("成功%s" %r.elapsed.seconds)
            global sus
            sus = sus + 1

        else:
            test.decrease(ips)
            #print("失败,异常结果为%s")


    except:
        test.decrease(ips)
        #print("异常结果为%s" %res)



'''检查端口是否关闭, 比较耗时'''
def isOpen(ip, port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False


if __name__ == "__main__":

    test = RedisClient()
    print(test.count())
    ip = test.batch(0, 160)
    js = []
    for ips in ip:

        IP = ips.getAddress() + ":" + str(ips.getPort())
        t = gevent.spawn(validIP, IP, "https://www.douban.com", ips, test)
        js.append(t)

    gevent.joinall(js)
    print(sus)
