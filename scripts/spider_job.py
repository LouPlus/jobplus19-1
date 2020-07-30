import scrapy

class JobSpider(scrapy.Spider):
    name = 'company'
#    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) \
         #   Gecko/20100101 Firefox/66.0'}

    def start_requests(self):
        urls = 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
#        for url in urls:
        yield scrapy.Request(url=urls, callback=self.parse)

    def parse(self, response):
        for j in response.xpath('//div[@class="dw_table"]/div[@class="el"]'):
            name = j.xpath('p/span/a/text()').extract_first()
            if name:
                yield{
                        'name' : name.strip(),
                        'location' : j.xpath('span[2]/text()').extract_first()
                    }
        '''
        css('span.company_content::text').extract_first()
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
        '''
