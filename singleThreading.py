from lxml import etree
import requests
import json

# 访问网页的请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.8"
}

# 存储解析后数据的本地文件
local_file = open("duanzi.json", "a")

# 解析 html字符串,获取需要信息
def parse_html(html):
    text = etree.HTML(html)

    # 返回所有段子的结点位置
    # contains模糊查询,第一个参数是要匹配的标签,第二个参数是标签名的部分内容
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

            local_file.write(json.dumps(items, ensure_ascii=False) + "\n")
        except:
            pass

def main():
    # 获取1-10页的网页源代码解析
    for page in range(1, 11):
        url = "https://www.qiushibaike.com/8hr/page/" + str(page) + "/"
        # 爬取网页源代码
        html = requests.get(url, headers=headers).text

        print("正在爬取："+url+"\n")
        parse_html(html)


if __name__ == "__main__":
    main()