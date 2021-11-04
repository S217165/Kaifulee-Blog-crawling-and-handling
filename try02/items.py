# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MuLuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    标题 = scrapy.Field()  # 文章标题
    时间 = scrapy.Field()  # 文章发表时间
    链接 = scrapy.Field()  # 文章详情页链接


class ShuJvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    链接 = scrapy.Field()  # 文章详情页链接
    收藏 = scrapy.Field()  # 收藏
    喜欢 = scrapy.Field()  # 喜欢
    阅读 = scrapy.Field()  # 阅读
    转载 = scrapy.Field()  # 转载
    评论 = scrapy.Field()  # 评论


class WenZhangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    标题 = scrapy.Field()  # 标题
    时间 = scrapy.Field()  # 时间
    标签 = scrapy.Field()  # 标签
    分类 = scrapy.Field()  # 分类
