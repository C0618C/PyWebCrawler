# 提供下载地址的下载类资源网站

'''
    跟网站结构相关的分析全抽离在这里，当网站改版时可以单独更新，而不影响主线策略
'''
import scrapy
from scrapy.contrib.loader import ItemLoader

from .url_setting import *
from .mySetting import *

class TrimAll(object):
    def __call__(self, values):
        vlist =[]
        for s in values:
            vlist.append(s.replace(' ','').replace('\r\n',''))
        return vlist

#主入口的主体 用于循环
def GetMainCrycle(response):
    return response.css('.k_list-lb')

#主入口页面的翻页、找下一页
def GetMainCrycle_NextPage(response):
    next_url = response.css('.k_pape').xpath('a[text()="下一页"]/@href').extract()
    if(len(next_url)>0):
        return scheme+allowed_domains[0]+next_url[0]
    else:
        return ''


# 爬文章列表 取标题、预览、文章实际地址、发起日期等信息
def Loader_index(self,item_selector):
    l = ItemLoader(item={}, selector = item_selector)

    conver_img=l.get_xpath('.//*[@class="lz_img"]/img/@src')

    l.add_xpath('title', './/*[@class="k_list-lb-2"]/div[1]/a[1]/text()')
    l.add_xpath('url', './/*[@class="k_list-lb-2"]/div[1]/a/@href')
    l.add_value('preview', conver_img)
    l.add_css('date', '#k_list-lb-2-f::text',re=r'(\d{4}-\d{2}-\d{2})')
    l.add_value('image_urls',conver_img)
    return l.load_item()


# 爬文章页 取标题、封面、预览、下载地址、发起日期信息
def Loader_content(response):
    l = ItemLoader(item={}, response = response)
    l.add_css('title','.k_jianjie-3a-1-name::text')
    l.add_xpath('preview','//*[@id="k_jianjie-2b"]/a/img/@src')
    l.add_value('date',l.get_xpath('//*[@class="k_jianjie-3a-2b"]/text()')[2])
    #l.add_value('url',_response.url[len(self._scheme+"//"+self.allowed_domains[0]):])
    l.add_css('down','.k_jianjie-3a-5down::text',TrimAll())
    l.add_xpath('images','//*[@class="content"]/p/img/@src')
    l.add_xpath('image_urls','//*[@class="content"]/p/img/@src')
    return l.load_item()

