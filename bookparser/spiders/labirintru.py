import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D1%81%D0%BF%D0%BE%D1%80%D1%82/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class='pagination-next']/a/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        books_links = response.xpath("//a[@class='product-title-link']/@href").extract()
        for book in books_links:
            yield response.follow(book, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        item_name = response.xpath("//h1/text()").extract_first()
        item_author = response.xpath("//*[@id='product-specs']/div[1]/div[1]/a/text()").extract_first()
        item_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        item_discount = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        item_rating = response.xpath("//div[@id='rate']/text()").extract_first()

        item = BookparserItem(link=response.url, name=item_name, author=item_author,
                              old_price=item_price, price=item_discount, rating=item_rating)
        yield item
