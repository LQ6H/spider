#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H

import requests
import threading
from lxml import etree
import json
from queue import Queue


# 采集网页页码队列是否为空的信号
CRAWL_EXIT=False

class ThreadCrawl(threading.Thread):
    def __init__(self,threadName,pageQueue,dataQueue):
        threading.Thread.__init__(self)
        # 线程名
        self.threadName=threadName
        # 页码队列
        self.pageQueue=pageQueue
        # 数据队列
        self.dataQueue=dataQueue

        self.headers="{'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}"

    def run(self):
        print("启动："+self.threadName)

        while not CRAWL_EXIT:
            try:
                # 从dataQueue中取出1一个页码数字,先进先出
                # 可选参数block,默认值是True
                # 如果队列为空,block为True,会进入阻塞状态,直到队列有新的数据
                # 如果队列为空,block为False,会弹出一个Queue.empty()异常
                page=self.pageQueue.get(False)
                # 构建网页的URL地址
                url="https://www.qiushibaike.com/8hr/page/"+str(page)+"/"
                content=requests.get(url,headers=self.headers).text

                # 将爬取到的网页源代码放入dataQueue队列中
                self.dataQueue.put(content)
            except:
                pass

        print("结束："+self.threadName)


PARSE_EXIT=False
class ThreadParse(threading.Thread):
    def __init__(self,threadName,dataQueue,localFile,lock):
        super(ThreadParse,self).__init__()
        # 线程名
        self.threadName=threadName
        # 数据队列
        self.dataQueue=dataQueue
        # 保存解析后数据的文件名
        self.localFile=localFile
        # 互斥锁
        self.lock=lock

    def run(self):
        print("启动："+self.threadName)
        while not PARSE_EXIT:
            try:
                html=self.dataQueue.get(False)
                self.parse(html)

            except:
                pass

        print("结束："+self.threadName)


    def parse(self,html):
        text = etree.HTML(html)
        node_list = text.xpath('//li[contains(@id,"qiushi_tag")]')

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


                # with后面有两个必须执行的操作：__enter__和__exit__,打开和关闭
                # 不管里面的操作如何,都会直接打开和关闭功能
                # 打开锁,向文件添加内容,释放锁

                with self.lock:
                    # 写入解析后的数据
                    self.localFile.write(json.dumps(items,ensure_ascii=False)+"\n")
                    self.localFile.close()
            except:
                pass

def main():
    # 页码队列,存储10个页码,先进先出
    pageQueue=Queue(10)
    for i in range(1,11):
        pageQueue.put(i)

    # 采集结果(网页的HTML源代码)的数据队列,参数为空表示不限制
    dataQueue=Queue()
    # 以追加的方式打开本地文件
    localFile=open("duanzi.json","wb+")
    # 互斥锁
    lock=threading.Lock()

    # 3个采集线程的名字
    crawlList=["采集线程1号","采集线程2号","采集线程3号"]
    # 创建,启动和存储3个采集线程
    threadCrawls=[]

    for threadName in crawlList:
        thread=ThreadCrawl(threadName,pageQueue,dataQueue)
        thread.start()
        threadCrawls.append(thread)

    # 3个解析线程的名字
    parseList=["解析线程1号","解析线程2号","解析线程3号"]
    # 创建,启动和存储3个解析线程
    threadParses=[]
    for threadName in parseList:
        thread=ThreadParse(threadName,dataQueue,localFile,lock)
        thread.start()
        threadParses.append(thread)

    while not pageQueue.empty():
        pass

    # 如果pageQueue为空,采集线程退出循环
    global CRAWL_EXIT
    CRAWL_EXIT=True

    print("pageQueue为空\n")

    for thread in threadCrawls:
        # 阻塞子线程
        thread.join()

    while not dataQueue.empty():
        pass

    print("dataQueue为空")

    global PARSE_EXIT
    PARSE_EXIT=True

    for thread in threadParses:
        thread.join()

    with lock:
        # 关闭文件,在关闭之前,内容都在内存里
        localFile.close()


if __name__=="__main__":
    main()



