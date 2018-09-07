# -*- coding: utf-8 -*-
# @Time    : 2018/9/7 0007 13:54
# @Author  : allenx555
# @FileName: main.py
# @Software: PyCharm
from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute('scrapy crawl acg'.split())
