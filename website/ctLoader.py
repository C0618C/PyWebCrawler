# 直接显示图片的漫画、插画类分享网站

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
    return response.css('.k_list-txt')

#主入口页面的翻页、找下一页
def Get_NextPage(response):
    next_url = response.css('.k_pape').xpath('a[text()="下一页"]/@href').extract()
    if len(next_url)>0:
        return scheme+allowed_domains[0]+next_url[0]
    else:
        return ''

#点击进去的地址
def GetContent_URL(item_selector):
    content_url = item_selector.xpath('./ul/li/a/@href').extract()
    if len(content_url) > 0 :
        return scheme+allowed_domains[0]+content_url[0]
    else:
        return ''

# 爬文章列表 取标题、预览、文章实际地址、发起日期等信息
def Loader_index(self,item_selector):
    l = ItemLoader(item={}, selector = item_selector)
    l.add_xpath('title', './ul/li/a/text()')
    l.add_xpath('url', './ul/li/a/@href')
    return l.load_item()


# 爬文章页 取标题、封面、预览、下载地址、发起日期信息
def Loader_content(response):
    l = ItemLoader(item={}, response = response)    
    sub_title=''
    if len(l.get_xpath('//*[@class="pagenow"]/text()'))>=1:
        sub_title += '-'+l.get_xpath('//*[@class="pagenow"]/text()')[0]
    l.add_value('title',l.get_xpath('//*[@class="b_list-1a-1c"]/text()')[0]+sub_title)
    l.add_xpath('content','//*[@class="content-img"]/p/img/@src')
    l.add_xpath('image_urls','//*[@class="content-img"]/p/img/@src')
    return l.load_item()

