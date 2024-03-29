import scrapy
import pymongo
import sys


class Scrapper(scrapy.Spider):
    name = 'Scraper'
    def __init__(self,url='', *args,**kwargs):
        super(Scrapper, self).__init__(*args, **kwargs)
        self.maxDepth=500
        self.item=0
        self.start_urls = url
    
    def parse(self, response):
        print(self.url)
        url = response.url
        title = response.url
        title = response.xpath("//title/text()").get()
        try:
            description = response.xpath("//meta[@name='description']/@content")[0].extract()
        except:
            description = "No Description Available"
        content = {'url':url,'title':title,'description':description}
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Indexed"]
        col = db["crawler"]
        col.insert_one(content)
        a_selectors = response.xpath("//a")
        for selector in a_selectors:
            text = selector.xpath("text()").extract_first()
            link = selector.xpath("@href").extract_first()
            request = response.follow(link, callback=self.parse)
            yield request
