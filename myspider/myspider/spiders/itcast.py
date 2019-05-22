# -*- coding: utf-8 -*-
import scrapy
from myspider.items import MyspiderItem

class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ('http://www.itcast.cn/channel/teacher.shtml',)

    def parse(self, response):
        items = []
        for each in response.xpath("//div[@class='li_txt']"):
            item = MyspiderItem()

            # 使用extract()方法返回的都是Unicode字符串
            name = each.xpath("h3/text()").extract()
            title = each.xpath("h4/text()").extract()
            info = each.xpath("p/text()").extract()

            # xpath返回的是包含一个元素的列表
            item["name"] = name[0]
            item["title"] = title[0]
            item["info"] = info[0]

            items.append(item)
            yield item



    """
        def parse(self, response):

    
        with open("teacher.html","w",encoding="utf-8") as file:
            file.write(response.text)
        pass
        
        items=[]
        for each in response.xpath("//div[@class='li_txt']"):
            item=MyspiderItem()

            # 使用extract()方法返回的都是Unicode字符串
            name=each.xpath("h3/text()").extract()
            title=each.xpath("h4/text()").extract()
            info=each.xpath("p/text()").extract()

            # xpath返回的是包含一个元素的列表
            item["name"]=name[0]
            item["title"]=title[0]
            item["info"]=info[0]

            items.append(item)

        return items

    
    
    
    """

