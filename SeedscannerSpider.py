import scrapy


class SeedscannerSpider(scrapy.Spider):
    name = "seeds"

    def start_requests(self):
        urls = ['https://grizzly-cannabis-seeds.co.uk/product-category/cup-winners/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
