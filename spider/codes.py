#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cookielib
import urllib
import urllib2
import json

import sys

import MySQLdb
import time

import re


class CodeSpider():
    """
    股票代码
    """
    base_url = "https://xueqiu.com"

    hq_url = "https://xueqiu.com/hq"

    # 代码url
    req_url = "https://xueqiu.com/service/v5/stock/screener/quote/list?size=30&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_=1566553350037&page="

    # 概念URL: ${code}例如002273  ${place} SZ, SH
    concept_url = """http://data.eastmoney.com/DataCenter_V3/stockdata/getData.ashx?url=HSO%2FLICO_CORETHEME&type=post&postData=%7B%22SecurityCode%22%3A%22${code}.${place}%22%7D&remove=SecinnerCode%2CSecurityCode%2CSecurityShortName%2CTradeMarketCode"""

    # 港资详情等
    detail_url = "http://www.gzyuwan.com/message_stock_detail.php?"  # code=600009&day=2019-08-22&rule=0

    # 短线策略
    short_strategy = {
        '强势上涨过程中，可逢低买进，暂不考虑做空': '买',
        '短期行情可能回暖，可适量买进股票，作短线反弹行情': '买',
        '该股处于空头行情中，可能有短期反弹': '买',
        '该股进入多头行情中，股价短线上涨概率较大': '买',

        '股价的强势特征已经确立，短线可能回调': '卖',
        '市场最近连续上涨中，短期小心回调': '卖',
        '短期的强势行情可能结束，投资者及时短线卖出、离场观望为宜': '卖',
        '市场单边上涨中，可短期持有为主，小心回调': '卖',
        '前期的强势行情已经结束，投资者及时卖出股票为为宜': '卖',
        '弱势下跌过程中，可逢高卖出，暂不考虑买进': '卖',

        '极度弱势行情中，投资者可暂时观望': '观望',
        '盘整震荡中，短期不宜操作': '观望',

    }

    # 中线策略
    medium_strategy = {
        '上涨趋势有所减缓，可适量高抛低吸': '买',
        '下跌有所减缓，仍应保持谨慎': '观望',
        '回落整理中且下跌有加速趋势': '卖',
        '回落整理中且下跌趋势有所减缓': '卖',
        '已发现中线买入信号': '买',
        '已发现中线卖出信号': '卖',
        '有加速上涨趋势': '买',
        '有加速下跌的趋势': '卖',
        '正处于反弹阶段': '买',
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

    def get_concept(self, symbol):
        """
        获取相关概念
        @:param symbol 代码 如SH600009
        :return:
        """
        code = symbol[-6:]
        place = symbol[0:2]
        req_url = self.concept_url.replace('${code}', code)
        req_url = req_url.replace('${place}', place)
        data = None
        request = urllib2.Request(req_url, data=data, headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read()

    def analyze_html(self):
        """
        解析网页html
        :return:
        """
        connect = self.get_db_connection()
        cur = connect.cursor()
        for i in range(130):
            try:
                print "\r\n", i, ":"
                # 分页获取股票代码
                url = self.req_url + str(i+1)
                response = self.get_html(url)
                res_json = json.loads(response)
                list_json = res_json["data"]["list"]
                for j in list_json:
                    try:
                        print j["symbol"], j["name"],  "\t\t",  # , j["id"]
                        # 获取北向资金动向
                        detail = self.get_detail(j["symbol"].replace('SH', '').replace('SZ', ''))
                        # print detail
                        northward_funds = re.findall(".* 净(.*)<.*", detail)  # 港资
                        northward_funds_days = re.findall(".*\..*([0-9])天.*", northward_funds[0])  # 港资连续增持天数
                        northward_funds_detail = '港资净%s' % str(northward_funds[0]) if len(northward_funds) > 1 else '未开通沪深股通'
                        northward_funds_days = '%s%s' % ('' if '增持' in str(northward_funds_detail) else '-',
                                                         str(northward_funds_days[0]) if len(northward_funds_days) > 0 else '0')
                        short = re.findall(".*短期趋势：(.*)。<br>中期.*", detail)  # 短线趋势
                        medium = re.findall(".*中期趋势：(.*)。<br>长期.*", detail)  # 中线趋势
                        short = str(short[0])if len(short) > 0 else ''
                        medium = str(medium[0])if len(medium) > 0 else ''
                        short_buy = self.short_strategy.get(short)
                        medium_buy = self.medium_strategy.get(medium)
                        # print short, '\r\n\r\n\r\n', medium, '\r\n\r\n\r\n'
                        # print northward_funds_days, northward_funds_detail, '\r\n\r\n\r\n',

                        # 获取相关概念
                        concept = self.get_concept(j["symbol"])
                        concept_json = json.loads(concept)
                        MainPointCon = ''
                        for concept_item in concept_json:
                            KeyWords = concept_item["KeyWords"]
                            MainPointConTemp = concept_item["MainPointCon"]
                            if "所属板块" == KeyWords:
                                MainPointCon = MainPointConTemp
                        sql = """insert into code(name, symbol, turnover_rate, concept, northward_funds_days, 
                            northward_funds_detail, short, medium, short_buy, medium_buy) 
                            values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"""
                        sql = sql % (j["name"], j["symbol"], j["turnover_rate"], MainPointCon, northward_funds_days, northward_funds_detail,
                                     short, medium, short_buy, medium_buy)
                        cur.execute(sql)
                    except Exception as e:
                        print e
                        pass
            except Exception as e:
                print e
                pass
        cur.close()
        connect.commit()

    def run(self):
        import sys
        reload(sys)
        sys.setdefaultencoding("utf-8")
        self.get_cookie()
        self.analyze_html()


CodeSpider().run()


