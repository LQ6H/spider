# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 名字
    name=scrapy.Field()
    # 图片链接
    image_link=scrapy.Field()
    # 图片保存地址
    image_path=scrapy.Field()

