import scrapy
import re

class CompanySpider(scrapy.Spider):
    name = 'company'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) \
            Gecko/20100101 Firefox/66.0'}

    def start_requests(self):
        urls = ['https://www.lagou.com/gongsi/{}.html'.format(i) 
                for i in range(55344, 55694, 5)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        name = response.css('h1.company_main_title a::text').extract_first()
        about = response.css('span.company_content::text').extract_first()
        about = about.strip() if about else ''
        if name:
            yield {
                'name': name.strip(),
                'description': response.css('h2.company_word::text'
                        ).extract_first().strip(),
                'logo': response.css('div.top_info_wrap img::attr(src)'
                        ).extract_first()[2:],
                'location': response.css('div#basic_container div.item_content li'
                        )[-1].css('span::text').extract_first(),
                'about': about.strip() if about else '',
                'tags': ', '.join([i.strip() for i in response.css('li.con_ul_li::text'
                        ).extract()])
            }
