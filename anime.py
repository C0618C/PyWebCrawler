import scrapy
import re
import _tgURL

# scrapy runspider anime.py -o o/idx.json

class AnimeSpider(scrapy.Spider):
    name = 'animespider'
    start_urls = _tgURL.target_url  #target_url= ['https://blog.scrapinghub.com']
    allowed_domains =[re.search('//([^/]*)/+',start_urls[0]).group(1)]
    _scheme = re.search('^https?:',start_urls[0]).group()

    def parse(self, response):
        for tt in response.selector.css('.k_list-lb'):  # 列表规则
            item = {}
            item['title'] = tt.xpath('.//*[@class="k_list-lb-2"]/div[1]/a/text()').extract()[0] # 标题
            item['url'] = tt.xpath('.//*[@class="k_list-lb-2"]/div[1]/a/@href').extract()[0] # 目标地址
            item['img'] = tt.xpath('.//*[@class="lz_img"]/img/@src').extract()[0]  #封面地址
            item['date']=tt.css('#k_list-lb-2-f::text').extract()[0][3:]  # 更新时间
            yield item
        
        # 翻页
        __next=response.selector.css('.k_pape').xpath('a[text()="下一页"]/@href').extract()
        if len(__next)>0:
            next_url = self._scheme+"//"+self.allowed_domains[0]+__next[0]
            self.log('Going to next page:\t '+next_url)
            yield scrapy.Request(next_url, callback=self.parse)

