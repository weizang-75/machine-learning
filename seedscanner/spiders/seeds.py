# -*- coding: utf-8 -*-
import scrapy


class SeedsSpider(scrapy.Spider):
    name = "seeds"
    allowed_domains = ["grizzly-cannabis-seeds.co.uk"]
    start_urls = [
        'https://grizzly-cannabis-seeds.co.uk/product-category/cup-winners/',
    ]

    def parse(self, response):
        for seed_url in response.css("article.product_pod > h3 > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(seed_url), callback=self.parse_seed_page)
        next_page = response.css("li.next > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_seed_page(self, response):
        item = {}
        product = response.css("div.product_main")
        item["title"] = product.css("h1 ::text").extract_first()
        item['category'] = response.xpath(
            "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
        ).extract_first()
        item['description'] = response.xpath(
            "//div[@id='product_description']/following-sibling::p/text()"
        ).extract_first()
        item['price'] = response.css('p.price_color ::text').extract_first()
        yield item
