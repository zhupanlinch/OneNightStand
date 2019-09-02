# OneNightStand
OneNightStand选股器，股票爬虫，每日获取所有个股的北向资金流入情况，以及日K的短线和中线趋势，作为短线选股的参考素材。

### 爬虫项目介绍

两市共3000多只股票，每次选股的时候都很痛苦。虽然，市面上有很多能够选股的软件，但是我用起来都不方便，不如自己把所有股票数据存到数据库，自己用起来更灵活。

1.从雪球上面爬所有股票代码和当日价格，换手率等指标

2.从东方财富上面获取个股的行业板块，概念板块等

3.从某网站上获取个股的北向资金加仓情况和个股的短期中期趋势

4.从雪球选股策略中爬当日选股策略

具体请参考codes.py

### 数据快照

![数据快照](https://github.com/zhupanlinch/OneNightStand/blob/master/%E6%95%B0%E6%8D%AE%E5%BF%AB%E7%85%A7.png)

### 部署介绍

阿里云服务器python2.7, crontab定时运行

0 6 * * * python /py/OneNightStand/spider/codes.py &
0 17 * * * python /py/OneNightStand/spider/short.py &

### 技术选型

#### 1.环境

python2.7

#### 2.主框架

python原生http请求框架和mysqldb框架

#### 3.数据库

mysql

### 欢迎赞赏
![赞赏](https://github.com/zhupanlinch/pay/blob/master/src/main/resources/static/common/%E8%B5%9E%E8%B5%8F%E7%A0%81.png)

