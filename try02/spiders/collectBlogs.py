# -*- coding: utf-8 -*-
import re
import scrapy
from try02.items import MuLuItem, WenZhangItem, ShuJvItem


class collectBlogsSpider(scrapy.Spider):
    name = 'collectBlogs'
    allowed_domains = ['blog.sina.com.cn']
    start_urls = ['http://blog.sina.com.cn/s/articlelist_1197161814_0_1.html']

    # 翻页
    def parse(self, response):
        # # 显示当前页数
        # num_url = response.xpath("//div[@class='SG_page']/ul/li[@class='SG_pgon']/text()").extract_first()
        # print("\n正在爬取第", num_url, "页")

        node_list = response.xpath('//div[@class="articleList"]')
        for node in node_list:
            item1 = MuLuItem()
            # 爬取目录页(标题、时间、链接)
            if node.xpath('//p[@class="atc_main SG_dot"]/span[2]/a/text()').extract():
                item1['标题'] = node.xpath('//p[@class="atc_main SG_dot"]/span[2]/a/text()').extract()
            if node.xpath('//p[@class="atc_info"]/span[2]/text()').extract():
                item1['时间'] = node.xpath('//p[@class="atc_info"]/span[2]/text()').extract()
            if node.xpath('//p[@class="atc_main SG_dot"]/span[2]/a/@href').extract():
                item1['链接'] = node.xpath('//p[@class="atc_main SG_dot"]/span[2]/a/@href').extract()
            yield item1

            # 爬取详情页数据
            for num in range(len(item1['链接'])):
                w = str(item1['链接'][num][-21:-13])
                q = str(item1['链接'][num][-11:-5])
                detail_url = 'http://comet.blog.sina.com.cn/api?maintype=num&uid=' + w + '&aids=' + q
                item2 = ShuJvItem()
                item2['链接'] = 'http://blog.sina.com.cn/s/blog_' + w + '01' + q + '.html'

                # 请求详情页动态数据(阅读数，喜欢数，评论数，转发数，收藏数)
                request = scrapy.Request(url=detail_url, callback=self.post_detail)
                request.meta['item2'] = item2
                yield request

                # 请求详情页静态数据(标题,时间,分类,标签)
                item3 = WenZhangItem()
                request1 = scrapy.Request(url=str(item1['链接'][num]), callback=self.post_detail2)
                request1.meta['item3'] = item3
                yield request1

        # # 显示当前页数
        # print("\n第", num_url, "页目录及详情页爬取完成")
        # 翻页
        next_url = response.xpath("//div[@class='SG_page']/ul/li[@class='SG_pgnext']/a/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)
        pass

    # 请求详情页动态数据(阅读数，喜欢数，评论数，转发数，收藏数)
    def post_detail(self, response):
        item2 = response.meta.get('item2')
        pattern = re.compile(r"\d+")
        reads = re.findall(pattern, response.text)

        if reads[-5]:
            item2['收藏'] = reads[-5]
        if reads[-4]:
            item2['喜欢'] = reads[-4]
        if reads[-3]:
            item2['阅读'] = reads[-3]
        if reads[-2]:
            item2['转载'] = reads[-2]
        if reads[-1]:
            item2['评论'] = reads[-1]
        yield item2

    # 请求详情页静态数据(标题,时间,分类,标签)
    def post_detail2(self, response):
        item3 = response.meta.get('item3')

        item3['标题'] = response.xpath('//div[@class="articalTitle"]/h2/text()').extract()
        item3['时间'] = response.xpath('//div[@class="articalTitle"]/span[2]/text()').extract()
        if response.xpath('//div[@class="articalTag"]/table/tr/td[@class="blog_class"]/a/text()').extract():
            item3['分类'] = response.xpath('//div[@class="articalTag"]/table/tr/td[@class="blog_class"]/a/text()').extract()
        if response.xpath('//div[@class="articalTag"]/table/tr/td[@class="blog_tag"]/h3/text()').extract():
            item3['标签'] = response.xpath('//div[@class="articalTag"]/table/tr/td[@class="blog_tag"]/h3/text()').extract()
        yield item3
