#使用Anaconda Prompt開啟檔案
#輸入scrapy crawl 'fileName'執行
#輸入scrapy crawl 'fileName' -o fileName.檔案類別 -t 檔案類別 ; -o代表等一下要輸出的檔案 -t是要用的格式
#抓取蘋果即時新聞文章

import scrapy
from bs4 import BeautifulSoup as BS
from firstProject.items import FirstprojectItem

class AppleNewsCrawler(scrapy.Spider):
    name = 'firstProject'
    start_urls = ['https://tw.appledaily.com/new/realtime'] #一定要取名為start_urls
    def parse(self, response):
        res = BS(response.body)
        for news in res.select('.rtddt'):
            #print(news.select('h1')[0].text)
            #print(news.select('a')[0]['href'])  #取得連結
            yield scrapy.Request(news.select('a')[0]['href'], self.parse_detail)    #進入到第二層頁面

    def parse_detail(self, response):
        res = BS(response.body)
        #宣告整理格式 items.py
        firstProjectitem = FirstprojectItem()
        firstProjectitem['title'] = res.select('h1')[0].text
        firstProjectitem['content'] = res.select('p')[0].text
        firstProjectitem['time'] = res.select('.ndArticle_creat')[0].text
        return firstProjectitem
