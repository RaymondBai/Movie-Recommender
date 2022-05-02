# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt0106145/']

    def parse(self, response):
        to_append = response.css('a.ipc-metadata-list-item__icon-link').attrib['href']
        cast_page = response.urljoin(to_append)
        yield scrapy.Request(cast_page, callback = self.parse_full_credits)
    
    def parse_full_credits(self, response):
        actor_relative_paths = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        for a in actor_relative_paths:
            yield scrapy.Request(response.urljoin(a), callback = self.parse_actor_page)
    
    def parse_actor_page(self, response):
        # find actor name
        actor_name = str(response.css('h1.header span.itemprop ::text')).split("data='")[-1].split("'")[0]
        # find list of films
        films = response.css('div.filmo-category-section div.filmo-row b a ::text').getall()
        for film in films:
            yield {
                "actor": actor_name,
                "movie_or_TV_name": film
                }
    

