import os
import re
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

from website.url_setting import *
from website.mySetting import *
from website.dwLoader import *

# scrapy runspider anime.py -o o/idx.json

class AnimeSpider(scrapy.Spider):
    name = proj_name
    start_urls = target_url  #['https://blog.scrapinghub.com']
    allowed_domains = allowed_domains
    _scheme = re.search('^https?:',start_urls[0]).group()

    _curPage=1

    custom_settings = {
        'FEED_URI': 'o/'+name+'/item_result.json'
        ,'FEED_EXPORT_ENCODING':'utf-8'
        ,'LOG_FILE':'o/'+name+'/scrapy.log'
        ,'ITEM_PIPELINES' : {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}     #照片下载管道
        ,'IMAGES_STORE' : 'o/'+name+'/image'              #照片保存位置
    }
    if os.path.exists('o/'+name) == False:
        os.mkdir('o/'+name)

    def parse(self, response):
        print(":::::::::::::::\t正在获取第 %d 页数据\t:::::::::::::::::::" % (self._curPage))
        return self.parse_content(response)


    def parse_index(self, response):        
        for tt in GetMainCrycle(response):  # 列表规则
            yield Loader_index(self,tt)            # 记录标题        
        yield self.GoToNextPage(response)

    def parse_content(self, response):
        for tt in GetMainCrycle(response):  # 列表规则
            next_url=GetContent_URL(tt)
            print('从目录打开网址：'+next_url)
            yield scrapy.Request(next_url, callback=self.parse_content_page)
        yield self.GoToNextPage(response)

    def parse_content_page(self,response):
        yield Loader_content(response)
        next_url=Get_NextPage(response)
        if len(next_url):
            print('翻到文章的下一页：'+next_url)
            yield scrapy.Request(next_url, callback=self.parse_content_page)

    
    # 翻页
    def GoToNextPage(self,response):
        next_url=Get_NextPage(response)
        if isDeep and len(next_url)>0:
            self._curPage+=1
            return scrapy.Request(next_url, callback=self.parse)
