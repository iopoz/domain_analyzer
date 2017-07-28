import scrapy
from scrapy import Selector


class DomainSpider(scrapy.Spider):
    name = 'domain_spider'
    start_urls = ['https://blog.scrapinghub.com']#['https://domainpunch.com/tlds/daily.php']

    def parse(self, response):

        items = Selector(response).css('h2.entry-title')#('#tablewrap td:nth-child(2)')
        for row in items:
            yield {'title': row.css('a ::text').extract_first()}#yield {'domain': row.extract()}

        # for next_page in response.css('#domtable_paginate > span > a'):
        #     yield response.follow(next_page, self.parse)

        for next_page in response.css('div.prev-post > a'):
            yield response.follow(next_page, self.parse)

