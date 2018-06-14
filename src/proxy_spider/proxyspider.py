#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- author by pekingzcc -*-
# -*- date : 2017-05-19 -*-

"""
run_spider():抓取并测试代理ip是否可以使用 抓取、测试网址均在config.py中设置
运行时创建一个线程用于抓取ip，其他50个线程用于检测ip可用性，结束后通过总线程写入
直接运行此文件将运行run_spider()
"""
from Utils.DBUtils import insertIPinfo
from Utils.redisdb import RedisClient
from Utils.IP import IP
import requests
import queue
import re
from lxml import html
from random import choice
import threading
import time

from proxy_spider.config import (
    PROXY_SITES_BY_REGX, PROXY_SITES_BY_XPATH, GOOD_OUTPUT_FILE, BAD_OUTPUT_FILE,
    USER_AGENT_LIST, RETRY_NUM, TIME_OUT, TEST_URL
)


class ProxySpider(object):
    """代理IP 爬虫"""
    def __init__(self):
        self.fetch_finish = False
        self.proxy_queue = queue.Queue()
        self.lock = threading.Lock()
        self.good_proxy = set()
        self.bad_proxy = set()
        self.count = 0

    """
       起一个线程将采集到的所有代理IP写入一个queue中
    """
    def in_proxy_queue(self):
        """
        根据正则直接获取代理IP 部分
        :return:
        """
        for site in PROXY_SITES_BY_REGX['urls']:
            resp = self._fetch(site)
            if resp is not None and resp.status_code == 200:
                try:
                    proxy_list = self._extract_by_regx(resp)
                    for proxy in proxy_list:
                        print("Get proxy %s and get into queue" % proxy)
                        ip, port = proxy.split(":")
                        self.proxy_queue.put((ip+" "+port+' -1'+' HTTP'))
                except Exception as e:
                    continue
        '''根据xpath 获取代理IP 部分'''
        for sites in PROXY_SITES_BY_XPATH:
            for site in sites['urls']:
                resp = self._fetch(site)
                print('Fetch', site)
                if resp is not None and resp.status_code == 200:
                    print('Success')
                    try:
                        proxy_list = self._extract_by_xpath(resp,
                                                            sites['ip_xpath'], sites['port_xpath'],
                                                            sites['anon_xpath'], sites['cat_xpath'],
                                                            sites['verify'])
                        for proxy in proxy_list:
                            print("Get proxy %s and get into queue" % proxy)
                            self.proxy_queue.put(proxy)
                    except Exception as e:
                        continue
                else:
                    print("%s Visiting failed" % site)
                    if resp is not None:
                        print('Error Code:', resp.status_code)
                    else:
                        print('Time Out')

        print("Get all proxy in queue!")
        self.fetch_finish = True
    """
        起多个线程取出queue中的代理IP 测试是否可用
    """
    def out_proxy_queue(self):

        while not self.fetch_finish:
            try:
                proxy = self.proxy_queue.get(timeout=1)
                self.count += 1
                # self._deduplicate_proxy(proxy)
                print("get proxy from queue")
                print(proxy)
                ip, port, anon, cat = proxy.split()
                check_proxy = self._fetch(TEST_URL, ip+":"+port)
                # check_proxy = proxy
                proxy_instance = IP(ip, int(port))
                proxy_instance.setCategory(cat)
                proxy_instance.setAnon(anon)
                if check_proxy and check_proxy.status_code == 200:
                    # resp_str = html.fromstring(check_proxy.text)
                    # http_via = resp_str.xpath(CHECK_PROXY_XPATH['HTTP_VIA'])
                    # http_x_forward_for = resp_str.xpath(CHECK_PROXY_XPATH['HTTP_X_FORWARDED_FOR'])
                    # try:
                    #     if http_via[0] == "anonymous / none" and http_x_forward_for[0] == "anonymous / none":
                    #         kwargs = {"ip_port": proxy, "anonymity_level": "Elite"}
                    #     elif http_via[0] and http_x_forward_for[0]:
                    #         kwargs = {"ip_port": proxy, "anonymity_level": "Anonymous"}
                    #     else:
                    #         kwargs = {"ip_port": proxy, "anonymity_level": "Transparent"}
                    # except IndexError:
                    #     print(check_proxy.text)
                    self._deduplicate_proxy(proxy_instance)
                    print('Success', proxy)
                else:
                    self._deduplicate_proxy(proxy_instance, False)
            except queue.Empty:
                continue

    """ 抓取代理网站函数"""
    def _fetch(self, url, proxy=None):
        kwargs = {
            "headers": {
                "User-Agent": choice(USER_AGENT_LIST),
            }, 
            "timeout": TIME_OUT,
            "verify": False,       
        }
        resp = None
        print("")
        for i in range(RETRY_NUM):
            try:
                if proxy is not None:
                    kwargs["proxies"] = {
                            "http": proxy}
                resp = requests.get(url, **kwargs)
                break
            except Exception as e:
                print("fetch %s  failed!\n%s , retry %d" % (url, str(e), i))
                time.sleep(1)
                continue
        return resp

    """ 根据解析抓取到的内容，得到代理IP"""
    def _extract_by_regx(self, resp):
        proxy_list = []
        if resp is not None:
            proxy_list = re.findall(PROXY_SITES_BY_REGX['proxy_regx'], resp.text)
        return proxy_list

    def _extract_by_xpath(self, resp, ip_xpath, port_xpath, anon_xpath, cat_xpath, verify):
        #import pdb;pdb.set_trace()
        proxy_list = []
        if resp is not None:
            resp = html.fromstring(resp.text)
            ip_list = resp.xpath(ip_xpath)
            port_list = resp.xpath(port_xpath)
            if anon_xpath != "":
                anon_list = resp.xpath(anon_xpath)
            else:
                anon_list = None
            if cat_xpath != "":
                cat_list = resp.xpath(cat_xpath)
            else:
                cat_list = None
            print(anon_list)
            print(verify)
            for i in range(len(ip_list)):
                if anon_list[i] == verify:
                    proxy = ip_list[i] + " " + port_list[i] + " " \
                            + "1" + " " \
                            + (cat_list[i] if cat_list else "HTTP")
                    print(proxy)
                    proxy_list.append(proxy)
        return proxy_list


    """ 输出可用的代理IP 到 set 中以达到去重"""
    def _deduplicate_proxy(self, proxy, ip_type=True):
        if not proxy:
            return
        if ip_type:
            with self.lock:
                self.good_proxy.add(proxy)
        else:
            with self.lock:
                self.bad_proxy.add(proxy)

    """ 持久化可用代理IP """
    def output_proxy(self):
        with open('./file/'+GOOD_OUTPUT_FILE, "w+") as proxy_file:
            proxy_file.write("%-30s%-30s%-30s%-30s\n" % ('IP', 'Port', 'Type', 'Anon'))
            for proxy in self.good_proxy:
                print("Write %s to proxy_list_good.txt\n" % proxy.getAddress())
                # proxy_file.write('%-30s%-30s%-30s%-30s\n'
                #                  % (proxy.getAddress(), proxy.getPort(), proxy.getCategory(), proxy.getAnon()))
                conn = RedisClient()
                conn.add(proxy)
                #insertIPinfo(proxy)

        # with open('./file/'+BAD_OUTPUT_FILE, "w+") as proxy_file:
        #     proxy_file.write("%-30s%-30s%-30s%-30s\n" % ('IP', 'Port', 'Type', 'Anon'))
        #     for proxy in self.bad_proxy:
        #         print("Write %s to proxy_list_bad.txt\n" % proxy.getAddress())
        #         proxy_file.write('%-30s%-30s%-30s%-30s\n'
        #                          % (proxy.getAddress(), proxy.getPort(), proxy.getCategory(), proxy.getAnon()))

    """一个线程用于抓取，多个线程用于测试"""
    def run(self):       
        threads = []
        in_proxy_queue_thread = threading.Thread(target=self.in_proxy_queue)
        out_proxy_queue_threads = [threading.Thread(target=self.out_proxy_queue) for i in range(50)]
        threads.append(in_proxy_queue_thread)
        threads.extend(out_proxy_queue_threads)
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]  
        """最终输出可用代理IP"""
        print('Try to write down IP address')
        self.output_proxy()
        print('No.', self.count)


def run_spider():
    spider = ProxySpider()
    spider.run()


def test_fetch():
    spider = ProxySpider()
    for site in PROXY_SITES_BY_XPATH[1]['urls']:
        resp = spider._fetch(site)
        if resp is not None and resp.status_code == 200:
            print('Success', site)
            list = spider._extract_by_xpath(resp, PROXY_SITES_BY_XPATH[1]['ip_xpath'],
                                     PROXY_SITES_BY_XPATH[1]['port_xpath'],
                                     PROXY_SITES_BY_XPATH[1]['anon_xpath'],
                                     PROXY_SITES_BY_XPATH[1]['cat_xpath'],
                                     PROXY_SITES_BY_XPATH[1]['verify'])
            for l in list:
                print(l)


if __name__ == "__main__":
    run_spider()
    # test_fetch()
