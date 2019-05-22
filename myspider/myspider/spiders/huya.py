# -*- coding: utf-8 -*-
import scrapy
from myspider.items import MyspiderItem


class HuyaSpider(scrapy.Spider):
    name = 'huya'
    allowed_domains = ['huya.com']
    start_urls = ['http://huya.com/g/2793',]

    def parse(self, response):
        items=[]
        for each in response.xpath("//li[@class='game-live-item']"):
            # 我们将得到的数据封装到一个myspiderHuya对象
            item=MyspiderItem()

            # extract 方法返回的都是Unicode字符串
            title=each.xpath("//a[@class='title new-clickstat']/text()")
            name=each.xpath("//i[@class='nick']/text()")
            people=each.xpath("//i[@class='js-num']/text()")

            # xpath返回的是包含一个元素的列表
        for i in range(len(title)):
            item["title"]=title[i]
            item["name"]=name[i]
            item["people"]=people[i]
            items.append(item)

        return items


