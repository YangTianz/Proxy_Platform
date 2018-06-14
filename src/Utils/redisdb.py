import redis
from Utils.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from Utils.settings import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from Utils.IP import *
from random import *
import re

"""
count获取ip总数
batch(start,end)分段获取ip，返回一个IP数组
decrease(IP) 减分，自动减1，到0抛出
"""

class RedisClient(object):
    def __init__(self, host = REDIS_HOST, port = REDIS_PORT, password = REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def random(self,k):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrevrange(REDIS_KEY, 0, 100)
        list = sample(result, k)
        ips = []
        for i in list:
            ips.append(self.translatetoIP(i))
        return ips

    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        ips = []
        result = self.db.zrevrange(REDIS_KEY, start, stop - 1)
        for i in result:
            ips.append(self.translatetoIP(i))
        return ips

    def add(self, IP, score=INITIAL_SCORE):
        proxy = self.translatetoproxy(IP)
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def decrease(self, IP):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        proxy = self.translatetoproxy(IP)
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减 1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def increase(self, IP, k):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        proxy = self.translatetoproxy(IP)
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score + k < MAX_SCORE:
            print('代理', proxy, '当前分数', score, '加', k)
            return self.db.zincrby(REDIS_KEY, proxy, k)

    def exists(self, IP):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        proxy = self.translatetoproxy(IP)
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, IP):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        proxy = self.translatetoproxy(IP)
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)

    def ipstatus(self):
        print("当前 IP 总数：", self.count())
        print("IP 分数分布: (越高越好)")
        print("1 ~ 10:  ", self.db.zcount(REDIS_KEY,1,10))
        print("11 ~ 20: ", self.db.zcount(REDIS_KEY, 11, 20))
        print("21 ~ 30: ", self.db.zcount(REDIS_KEY, 21, 30))
        print("31 ~ 40: ", self.db.zcount(REDIS_KEY, 31, 40))
        print("41 ~ 50: ", self.db.zcount(REDIS_KEY, 41, 50))
        print("51 ~ 60: ", self.db.zcount(REDIS_KEY, 51, 60))
        print("61 ~ 70: ", self.db.zcount(REDIS_KEY, 61, 70))
        print("71 ~ 80: ", self.db.zcount(REDIS_KEY, 71, 80))
        print("81 ~ 90: ", self.db.zcount(REDIS_KEY, 81, 90))
        print("91 ~ 100:", self.db.zcount(REDIS_KEY, 91, 100))
        print("只有分数大于 20 的 IP 地址会被使用")

    def translatetoproxy(self, IP):
        proxy = IP.getAddress()
        proxy += ':'
        proxy += str(IP.getPort())
        if IP.getCategory()!="":
            proxy += ':'
            proxy += str(IP.getCategory())
        return proxy

    def translatetoIP(self, proxy):
        proxy = str.split(proxy,':')
        a = IP(proxy[0],int(proxy[1]))
        if len(proxy)>2:
            a.setCategory(proxy[2])
        return a


