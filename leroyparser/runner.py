from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroyparser import settings
from leroyparser.spiders.leroyru import LeroyruSpider

import sys

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # sys.argv[1]

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroyruSpider)

    process.start()

