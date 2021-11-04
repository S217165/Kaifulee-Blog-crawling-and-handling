# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import json
import re
import sys
import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from try02.items import *


def chuli(item):
    if isinstance(item, WenZhangItem):
        adapter = ItemAdapter(item)
        old_bt = adapter['标题']
        old_sj = adapter['时间']
        # 处理标题：去除标题中的\xa0、\u200b、\u3000
        try:
            if str(adapter['标题']) != "":
                move = dict.fromkeys((ord(c) for c in u"\xa0\u200b\u3000"))
                new = adapter['标题'][0].translate(move)  # new 是字符串
                adapter['标题'] = new.split('\n')  # 转为列表
                if str(old_bt) != str(adapter['标题']):
                    print("有问题的的标题", old_bt)
                    print("处理后的结果", adapter['标题'])
            else:
                raise DropItem(f"{item}该项缺乏标题")
        except:
            raise DropItem(f"{item}该项缺乏标题")

        # 处理时间：丢弃没有时间的 item, 将时间外的小括号去除
        try:
            # (2015-02-15 21:30:41)——去掉小括号，利用正则表达式匹配
            # print("前",adapter['时间'])
            # 前['\n\t\t\t\t', '\t\n\t\t\t']
            # 后[]
            if adapter['时间'] != ['\n\t\t\t\t', '\t\n\t\t\t']:
                adapter['时间'] = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})", str(adapter['时间']))
                # print("后",adapter['时间'])
            else:
                raise DropItem(f"{item}该项缺乏时间")
            # 由于带括号的时间数目过多，为减少
            if old_sj != adapter['时间']:
                print("\n处理前的时间数据为：", old_sj)
                print("处理后的时间数据为：", adapter['时间'])
        except:
            raise DropItem(f"{item}该项缺乏时间")

    return item


class collectBlogsPipeline(object):
    progress = 0

    def open_spider(self, spider):
        # 打开/创建 csv 文件
        self.f1 = open("文章.csv", "w", encoding='utf-8')
        self.f2 = open("数据.csv", "w", encoding='utf-8')
        self.f3 = open("目录.csv", "w", encoding='utf-8')

        # 准备 mongodb
        host = spider.settings.get("MONGODB_HOST", "localhost")
        port = spider.settings.get("MONGODB_PORT", 27017)
        db_name = spider.settings.get("MONGODB_NAME", "mydb2")
        collecton_name_one = spider.settings.get("MONGODB_COLLECTON", "文章")
        collecton_name_two = spider.settings.get("MONGODB_COLLECTON", "数据")
        collecton_name_three = spider.settings.get("MONGODB_COLLECTON", "目录")
        # 连接Mongodb,得到一个客户端对象
        self.db_client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库，得到一个数据库对象
        self.db = self.db_client[db_name]
        # 指定集合，得到一个集合对象
        self.db_collecton1 = self.db[collecton_name_one]
        self.db_collecton2 = self.db[collecton_name_two]
        self.db_collecton3 = self.db[collecton_name_three]

    def process_item(self, item, spider):
        # 显示进度条
        self.progress += 1
        print("\r", end="\r")
        # 5.1是因为函数共运行510次，10是由于进度条显示效果太长，所以改为5，都是通过测试得出的，不能通用
        print("总程序进度: {:.2f}%: ,正在写入数据".format(self.progress / 5.1), "▋" * (self.progress // 7), end="\r")
        # 刷新缓冲区
        sys.stdout.flush()

        if isinstance(item, WenZhangItem):
            chuli(item)

            item_dict = dict(item)  # 将item转换成字典
            self.db_collecton1.insert_one(item_dict)  # 将数据插入到集合

        elif isinstance(item, ShuJvItem):
            item_dict = dict(item)
            self.db_collecton2.insert_one(item_dict)

        elif isinstance(item, MuLuItem):
            item_dict = dict(item)
            self.db_collecton3.insert_one(item_dict)

        # 将数据存入csv文件
        if isinstance(item, WenZhangItem):
            chuli(item)

            content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.f1.write(content)

        elif isinstance(item, ShuJvItem):
            content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.f2.write(content)

        elif isinstance(item, MuLuItem):
            content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.f3.write(content)

    def close_spider(self, spider):
        self.db_client.close()
        self.f1.close()
        self.f2.close()
        self.f3.close()
