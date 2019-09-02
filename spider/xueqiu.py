#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cookielib
import urllib2
import json

import sys


class XueqiuSpider():
    """
    雪球
    """
    base_url = "https://xueqiu.com"

    hq_url = "https://xueqiu.com/hq"

    req_url = {
               "关注热门": "https://xueqiu.com/stock/screener/screen.json?category=SH&size=10&order=desc&orderby=follow&current=ALL&follow=ALL&follow7d=ALL&pct=ALL&_=1502077154988",
               "讨论热门": "https://xueqiu.com/stock/screener/screen.json?category=SH&size=10&order=desc&orderby=tweet&current=ALL&tweet=ALL&tweet7d=ALL&pct=ALL&_=1502080936642",
               "交易热门": "https://xueqiu.com/stock/screener/screen.json?category=SH&size=10&order=desc&orderby=deal&current=ALL&deal=ALL&deal7d=ALL&pct=ALL&_=1502080999021",
               "本周关注热门": "https://xueqiu.com/stock/screener/screen.json?category=SH&size=10&order=desc&orderby=follow7d&current=ALL&follow=ALL&follow7d=ALL&pct=ALL&_=1502091915340",
               "本周讨论热门": "https://xueqiu.com/stock/screener/screen.json?category=SH&size=10&order=desc&orderby=tweet7d&current=ALL&tweet=ALL&tweet7d=ALL&pct=ALL&_=1502091958927",
               "本周交易热门": "https://xueqiu.com/stock/screener/screen.json?category=SH&size=10&order=desc&orderby=deal7d&current=ALL&deal=ALL&deal7d=ALL&pct=ALL&_=1502091982499"
               }

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
        for i in self.req_url:
            print "\r\n", i, ":"
            url = self.req_url.get(i)
            response = self.get_html(url)
            res_json = json.loads(response)
            list_json = res_json["list"]
            for j in list_json:
                print j["symbol"], j["name"],  "\t\t",  # , j["id"]

    def run(self):
        self.get_cookie()
        self.analyze_html()


XueqiuSpider().run()

