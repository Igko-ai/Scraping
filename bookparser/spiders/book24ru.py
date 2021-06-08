import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D1%81%D0%BF%D0%BE%D1%80%D1%82']
    page = 1

    def parse(self, response: HtmlResponse):
        self.page += 1
        next_page = f'https://book24.ru/search/page-{self.page}/?q=%D1%81%D0%BF%D0%BE%D1%80%D1%82'
        if not response.xpath("//div[@class='search-page__desc']/text()[contains(., 'К сожалению, по вашему запросу')]"):
            yield response.follow(next_page, callback=self.parse)

        books_links = response.xpath("//a[@class='product-card__name smartLink']/@href").extract()
        for book in books_links:
            yield response.follow(book, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        item_name = response.xpath("//h1[@class='item-detail__title']/text()").extract_first()
        item_author = response.xpath("//a[@class='item-tab__chars-link js-data-link']/text()").extract_first()
        item_old_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        item_price = response.xpath("//b[@itemprop='price']/text()").extract_first()
        item_rating = response.xpath("//span[@itemprop='ratingValue']/text()").extract_first()

        item = BookparserItem(link=response.url, name=item_name, author=item_author,
                            old_price=item_old_price, price=item_price, rating=item_rating)
        yield item