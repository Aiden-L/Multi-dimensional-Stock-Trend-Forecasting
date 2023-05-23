import json

import requests
from lxml import etree

STOCK_CODE = '600030'
PAGE = 50


# 根据股票代码爬取资讯，并将【内容，作者，时间】信息存入csv文件
def gettext(codestr):
    with open("data/" + codestr + "news.csv",'w',encoding="utf-8") as f:
        for i in range(PAGE):
            try:
                url = 'http://guba.eastmoney.com/list,' + codestr + ',1,f_' + str(i) + '.html'

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
                }

                response = requests.get(url=url, headers=headers)

                html_tree = etree.HTML(response.text)

                news_divs = html_tree.xpath('//*[@id="articlelistnew"]//div[@class="articleh normal_post"]')


                for news_div in news_divs:
                    title = news_div.xpath('./span[3]/a/text()')
                    author = news_div.xpath('./span[4]/a/font/text()')
                    time = news_div.xpath('./span[5]/text()')
                    if title[0] and author[0] and time[0]:
                        f.write(title[0] + ',' + author[0] + ',' + time[0] + '\n')
            except Exception as e:
                print("Error:", e)


# 读取存储沪深300股票代码json，分别爬取
def get300text():
    with open("300code.json", 'r') as f:
        codes = json.loads(f.read())
    count = 0
    for code in codes:
        count += 1
        print("正在获取数据"+code+"["+str(count)+"/300]")
        gettext(code)


if __name__ == '__main__':
    # gettext(STOCK_CODE)
    get300text()

