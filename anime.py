import scrapy
import tgURL

class AnimeSpider(scrapy.Spider):
    name = 'animespider'
    start_urls = tgURL.target_url
    print(start_urls)
    def parse(self, response):
        pass