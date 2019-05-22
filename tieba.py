#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H

import urllib.request

def tieba_spider(url,begin_page,end_page):
    """
    :param url: 网页地址
    :param begin_page: 起始页
    :param end_page: 结束页
    :return: url文件
    """
    for page in range(begin_page,end_page+1):
        pn=(page-1)*50
        file_name="第"+str(page)+"页.html"
        full_url=url+"&pn="+str(pn)
        html=load_page(full_url,file_name)
        write_page(html,file_name)

def load_page(url,filename):
    """
    :param url: 爬取url地址
    :param filename: 文件名
    :return: 网页内容
    """
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
    }

    request=urllib.request.Request(url,headers=headers)
    return urllib.request.urlopen(request).read()

def write_page(html,filename):
    """
    :param html: 网页内容
    :param filename: 文件名
    :return:
    """
    print("正在保存"+filename)

    with open(filename,"w") as file:
        file.write(html.decode("utf-8"))

