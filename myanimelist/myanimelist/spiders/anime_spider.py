import scrapy

class AnimeSpider(scrapy.Spider):
    name = "anime"
    start_urls = ['https://myanimelist.net/topanime.php']    

    def parse(self,response):
        contents= response.css('div.pb12 table tr.ranking-list')
        for content in contents:
            yield {
                'title' : content.css('div.detail h3 a::text').get(),
                'type' : content.css('div.detail div.information::text').getall()[0].replace('\n        ',''),
                'date' : content.css('div.detail div.information::text').getall()[1].replace('\n        ',''),
                'vote_count' : content.css('div.detail div.information::text').getall()[2].replace('\n        ',''),
                'score' : content.css('div.js-top-ranking-score-col span.text::text').get(),
            }
        next_page = response.css('div.pb12 div.di-b.ac.pt16 a.next').attrib['href']
        if next_page:
            yield response.follow(next_page, callback=self.parse)