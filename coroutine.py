#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H


import requests
from queue import Queue
import time
from lxml import etree
import gevent

class Spider(object):
    def __init__(self):
        self.headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
        }

        self.base_url="https://www.qiushibaike.com/8hr/page/"
        # 创建保存数据的队列
        self.data_queue=Queue()
        # 统计数量
        self.count=0

    def send_request(self,url):
        print("[INFO]：正在爬取"+url)
        html=requests.get(url,headers=self.headers).content
        # 每次请求间隔1s
        time.sleep(1)
        self.parse_page(html)

    def parse_page(self,html):
        html_ogj=etree.HTML(html)
        node_list=html_ogj.xpath('//li[contains(@id,"qiushi_tag")]')

        for node in node_list:
            try:

                # 获取用户名
                username = node.xpath('.//span[@class="recmd-name"]/text()')

                # 图片链接
                image = node.xpath('.//img/@src')[0]

                # 段子内容
                content = node.xpath('.//a[@class="recmd-content"]')[0].text

                # 点赞
                like = node.xpath('.//div[@class="recmd-num"]/span')[0].text

                # 评论
                try:
                    comments = node.xpath('.//div[@class="recmd-num"]/span')[3].text
                except IndexError:
                    comments = 0

                items = {
                    "username": username,
                    "image": image,
                    "content": content,
                    "like": like,
                    "comments": comments
                }

                self.count+=1
                self.data_queue.put(items)
            except:
                pass

    def start_work(self):
        job_list=[]
        for page in range(1,11):
            # 构建一个协程任务对象
            url=self.base_url+str(page)+"/"
            job=gevent.spawn(self.send_request,url)

            # 保存所有的协程任务
            job_list.append(job)

        # joinall()接收一个列表,将列表中的所有协程任务添加到任务队列里执行
        gevent.joinall(job_list)

        local_file=open("duanzi.json","wb+")

        while not self.data_queue.empty():
            content=self.data_queue.get()
            result=str(content).encode("utf-8")
            local_file.write(result+b"\n")

        local_file.close()
        print(self.count)

if __name__=="__main__":
    spider=Spider()
    spider.start_work()

