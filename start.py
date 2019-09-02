#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading

from spider.laotie import laotie_spider


def laotie_timer(seconds=10):
    laotie_spider().run()
    print "======================================================\r\n\r\n"
    # 定时器,参数为(多少时间后执行，单位为秒，执行的方法)
    timer = threading.Timer(seconds, laotie_timer)
    timer.start()

if __name__ == '__main__':
    laotie_timer()

