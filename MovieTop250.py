#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H


import urllib.request
from pymongo.mongo_client import MongoClient
from bs4 import BeautifulSoup

def douban():
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"

    headers={
        "User-Agent":user_agent
    }

    base_url="https://movie.douban.com/top250?start="

    for i in range(0,10):
        full_url=base_url+str(i*25)

        request=urllib.request.Request(full_url,headers=headers)
        response=urllib.request.urlopen(request)
        html=response.read()
        # print(html)

        # 选取符合要求的节点信息
        soup=BeautifulSoup(html,"lxml")
        div_list=soup.find_all("div",{"class":"info"})

        for node in div_list:
            # 电影名称
            title=node.find("a").find("span").text
            # 电影评分
            score=node.find("div",class_="star").find("span",class_="rating_num").text+"分"
            # 详情链接
            link=node.find("a")["href"]

            data_dict={"电影":title,"评分":score,"链接":link}

            client=MongoClient("localhost",27017)
            db=client.test
            collection=db.movie

            # 逐条往集合插入文档
            collection.insert_one(data_dict)

            # 查找score等于9.2的文档
            cursor=collection.find({"评分":"9.2分"})
            print(cursor)


if __name__=="__main__":
    douban()


