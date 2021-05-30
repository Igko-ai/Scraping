import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroyruSpider(scrapy.Spider):
    name = 'leroyru'
    allowed_domains = ['leroymerlin.ru']
    urls = ['https://leroymerlin.ru/search/?q=%D0%9E%D0%B1%D0%BE%D0%B8']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@aria-label, 'Следующая страница')]/@href")
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        goods_links = response.xpath("//a[@data-qa='product-name']/@href")
        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)

    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)

        loader.add_value('link', response.url)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//img[@alt='image thumb']/@src")
        loader.add_xpath('price, "//span[@slot="price"]/text()')
        loader.add_xpath('parameters', "//d1[@class='def-list']")

        yield loader.load_item()

