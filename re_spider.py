#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H


import urllib.request
import re

class Spider(object):
    def __init__(self):
        # 起始页位置
        self.begin_page=int(input("请输入起始页："))
        self.end_page=int(input("请输入终止页："))


    def load_page(self):

        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"

        headers={
            "User-Agent":user_agent
        }

        for page in range(self.begin_page,self.end_page+1):
            base_url="https://www.zhipin.com/c101200100/?query=python&page="+str(page)

            request=urllib.request.Request(base_url,headers=headers)

            response=urllib.request.urlopen(request)

            html=response.read().decode("utf-8")

            print(html)

    def lxml_parse_page(self,html):
        """
        :param html: 待解析网页
        :return: 工作信息列表
        """
        from lxml import etree

        # 从字符串中解析HTML文档或片段,返回根节点
        root=etree.HTML(html)

        # 查找所有职位连接
        links = root.xpath("//div[@class='info-primary']/h3/a/@href")

        # 查找所有职位名称
        names = root.xpath("//div[@class='job-title']/text()")

        # 查看所有工作地点
        locations = root.xpath("//div[@class='info-primary']/p/text()[1]")

        # 查看所有薪资
        moneys = root.xpath("//h3[@class='name']/a/span/text()")

        # 定义空列表,以保存元素信息
        items=[]
        for i in range(0,len(names)):
            item={}

            url="https://www.zhipin.com/"
            item["职位名称"]=names[i]
            item["详情连接"]=url+links[i]
            item["工作地点"]=locations[i]
            item["薪资范围"]=moneys[i]
            items.append(item)
        print(items)




