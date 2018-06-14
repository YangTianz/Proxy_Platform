import redis
from Utils.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from Utils.settings import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from Utils.IP import *
import re

class RedisClient(object):
    def __init__(self, host = REDIS_HOST, port = REDIS_PORT, password = REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

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


    def translatetoproxy(self, IP):
        proxy = IP.getAddress()
        proxy += ':'
        proxy += str(IP.getPort())
        return proxy

    def translatetoIP(self, proxy):
        proxy = str.split(proxy,':')
        a = IP(proxy[0],int(proxy[1]))
        return a

