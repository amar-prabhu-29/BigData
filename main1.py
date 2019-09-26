import scrapy

class Scrapper(scrapy.Spider):
    name="Scraper"
    start_urls=['http://www.aide2019.in']

    def parse(self, response):
        print("URL Being Crawled:"+response.url)
        meta_selectors = response.xpath("//meta")
        for selector in meta_selectors:
            text = selector.xpath("text()").extract_first()
            type_meta = selector.xpath("@name").extract_first()
            flag=False
            if(type_meta == 'description'):
                flag = True
                print("Index Terms:"+selector.xpath("@content").extract_first())
            if(flag == False):
                print("No Data To Index Avaiable")
        print("\n\n")
            
        a_selectors = response.xpath("//a")
        for selector in a_selectors:
            text = selector.xpath("text()").extract_first()
            link = selector.xpath("@href").extract_first()
            request = response.follow(link, callback=self.parse)
            yield request