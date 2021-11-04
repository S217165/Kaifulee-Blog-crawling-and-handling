#!/usr/bin/env python
"""
-- coding: utf-8 --
@Time : 2021/9/27 19:38
@Author : ZhaoJie
@File : main.py
@Software : PyCharm
@D6esc :用于Scrapy调试
@Contact :1303622496@qq.com
"""

from scrapy.cmdline import execute
import sys
import os

print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "collectBlogs"])
