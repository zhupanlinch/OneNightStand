#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cookielib
import urllib2
import json

import sys

import time


class laotie_spider():
    """
    老铁的雪球
    """
    base_url = "https://xueqiu.com"

    hq_url = "https://xueqiu.com/hq"

    req_url = [
               "https://xueqiu.com/v4/statuses/user_timeline.json?page=1&user_id=8368332440"
               ]

    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

    cookie = {}

    def __init__(self):
        pass

    def get_cookie(self):
        """
        获取cookie
        :return:
        """
        cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        req = urllib2.Request(self.base_url, headers=self.headers)
        response = opener.open(req).read()
        self.cookie = cookie

    def get_html(self, url):
        """
        获取网页html
        :return:
        """
        req = urllib2.Request(url, headers=self.headers)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        response = opener.open(req)
        return response.read()

    def analyze_html(self):
        """
        解析网页html
        :return:
        """
        today = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
        print time.strftime("%Y-%m-%d %H:%M:%S ..........................................", time.localtime(int(time.time())))
        for i in self.req_url:
            # print "\r\n", i, ":"
            url = i
            response = self.get_html(url)
            res_json = json.loads(response)
            list_json = res_json["statuses"]
            for j in list_json:
                create_at = time.strftime("%Y-%m-%d", time.localtime(j["created_at"]/1000))
                if create_at == today:
                    print create_at, j["created_at"],  j["text"], "\r\n\r\n",  # , j["id"]

    def run(self):
        self.get_cookie()
        self.analyze_html()


laotie_spider().run()

