# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt8946378/']

    def parse(self, response):
        to_append = response.css('a.ipc-metadata-list-item__icon-link').attrib['href']
        cast_page = response.urljoin(to_append)
        yield scrapy.Request(cast_page, callback = self.parse_full_credits)
    
    def parse_full_credits(self, response):
        actor_relative_paths = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        for a in actor_relative_paths:
            yield {"path": response.urljoin(a)}

