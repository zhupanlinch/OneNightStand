#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cookielib
import urllib
import urllib2
import json
import time
import re

import MySQLdb


class short_spider():
    """
    雪球选股
    """
    base_url = "https://xueqiu.com"

    hq_url = "https://xueqiu.com/hq"

    req_url = "https://xueqiu.com/v4/statuses/user_timeline.json?user_id=9796081404&page="

    detail_url = "http://www.gzyuwan.com/message_stock_detail.php?"  # code=600009&day=2019-08-22&rule=0

    kline_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=${symbol}&begin=${begin}&period=day&type=before&count=-142"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

    cookie = {}

    def __init__(self):
        pass

    def get_db_connection(self):
        """
        获取数据库连接
        :return:
        """
        conn = MySQLdb.connect(
            host='123.207.243.40',
            port=3306,
            user='root',
            passwd='jupanshuai2018',
            db='money',
            charset="utf8"
        )
        return conn

    def save_to_db(self):
        sql = ''
        connect = self.get_db_connection()
        cur = connect.cursor()
        cur.execute(sql)
        cur.close()
        connect.commit()

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

    def get_detail(self, code):
        """
        获取港资情况，概念板块
        @:param code 代码 如600009
        :return:
        """
        formate = {
            "code": code,
            "day": time.strftime("%Y-%m-%d", time.localtime(int(time.time()))),
            "rule": "0"
        }
        data = urllib.urlencode(formate)
        request = urllib2.Request(self.detail_url, data=data, headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read()

    def analyze_html(self):
        """
        解析网页html
        :return:
        """
        today = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
        print time.strftime("%Y-%m-%d %H:%M:%S ......", time.localtime(int(time.time())))
        connect = self.get_db_connection()
        cur = connect.cursor()
        for i in range(5):
            print '正在获取第%d页的数据' % (i + 1)
            url = self.req_url + str(i + 1)
            response = self.get_html(url)
            res_json = json.loads(response)
            list_json = res_json["statuses"]
            for j in list_json:
                create_at = time.strftime("%Y-%m-%d", time.localtime(j["created_at"]/1000))
                if create_at == today:
                    type = re.findall(".*#(.*)#.*", j["text"])
                    name_symbol = re.findall(".*\$(.*)\$.*", j["text"])
                    name = re.findall("(.*)\(.*", name_symbol[0])
                    symbol = re.findall(".*\((.*)\).*", name_symbol[0])
                    print name_symbol[0], type[0], symbol[0],  "\r\n"

                    detail = self.get_detail(symbol[0].replace('SH', '').replace('SZ', ''))
                    # print detail
                    northward_funds = re.findall(".* 净(.*)<.*", detail)  # 港资
                    northward_funds_days = re.findall(".*\..*([0-9])天.*", northward_funds[0])  # 港资连续增持天数
                    # concept1 = re.findall(".*行业:(.*)<br.*", detail)  # 行业板块
                    # concept2 = re.findall(".*概念:(.*)", detail)  # 概念板块
                    # if len(concept2) > 0:
                    #     match_obj = re.match(u"[\u4e00-\u9fa5]+", concept2[0])
                    #     if match_obj:
                    #         print match_obj.group()
                    #
                    # concept2 = re.findall(".*(\u4E00-\u9FA5).*", concept2[0]) if len(concept2) > 0 else []
                    # print str(concept1[0]), concept2
                    northward_funds_detail = '港资净%s' % str(northward_funds[0]) if len(northward_funds) > 1 else '未开通沪深股通'
                    northward_funds_days = '%s%s' % ('' if '增持' in str(northward_funds_detail) else '-', str(northward_funds_days[0]) if len(northward_funds_days) > 0 else '0')
                    print northward_funds_days, northward_funds_detail, '\r\n\r\n\r\n',

                    sql = """insert into one_night_stand(name, symbol, type, northward_funds_day, 
                          northward_funds_detail) values(\'%s\',\'%s\',\'%s\',%s,\'%s\')"""
                    # sql = sql % (name[0], symbol[0], type[0], northward_funds_days, northward_funds_detail)
                    sql = sql % (name[0], symbol[0], type[0], northward_funds_days, str(northward_funds_detail))
                    cur.execute(sql)
                    # print j["text"], "\r\n",  # , j["id"]
        cur.close()
        connect.commit()

    def run(self):
        import sys
        reload(sys)
        sys.setdefaultencoding("utf-8")
        self.get_cookie()
        self.analyze_html()


short_spider().run()

