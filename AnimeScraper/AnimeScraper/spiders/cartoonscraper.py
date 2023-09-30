import scrapy


class CartoonscraperSpider(scrapy.Spider):
    name = "cartoonscraper"
    allowed_domains = ["aniwatch.to"]
    start_urls = ["https://aniwatch.to"]

    def parse(self, response):
        pass
