import requests, socket
from Utils.DBUtils import *
import re
requests.adapters.DEFAULT_RETRIES = 5       #设置最大重连次数
socket.setdefaulttimeout(20)        #设置默认超时时间

'''访问微博'''
def validWeibo():
    r = requests.get("")
    pass

'''访问知乎'''
def validZhihu():
    r = requests.get("")
    pass

'''访问豆瓣'''
def validDouban():
    r = requests.get("")
    pass

'''访问StackOverflow'''
def validStackOverflow():
    r = requests.get("")
    pass

'''访问B站'''
def validBili():
    r = requests.get("")
    pass

def validIP():

    '''
    从数据库中拿到IP，确保可以访问其ip和port
    期望有一个column记录当前port被关闭的次数
    '''

    checkList = showAllIP()      # 从数据库中提取的本次需要校验的IP
    for IP in checkList:
        print(IP)

    '''检查IP可用性'''
    for IP in checkList:
        # 设置IP为代理
        proxies = {         #保证IP的格式正确(str?)
            'http': IP,
            'https': IP,
        }
        ip = re.split(":", IP)[0]
        port = re.split(":", IP)[1]

        '''一次基础校验'''
        try:
            r = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)      #设置超时
            if r.status_code == 200:
                #ttt = r.elapsed.seconds
                TTT = r.elapsed.microseconds
                #print("响应时间%s" %ttt)
                print("响应时间%s" %TTT)
                changeIP_AN(-1, ip, port)

                continue

            else:
                changeIP_AN(1,ip,port)
                continue        # 进行删除或放到另一个table或计数
        except:
            changeIP_AN(1, ip, port)
            print("访问超时，检查端口是否关闭")
            # if isOpen("221.228.17.172", 8181) == True:
            #     print("端口并没有关闭")
            # else:
            #     print("端口都关了")
                            # 同上

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
    validIP()
