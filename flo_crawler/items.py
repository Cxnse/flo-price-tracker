import scrapy

class FloCrawlerItem(scrapy.Item):
    product_id = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    discount_rate = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    timestamp = scrapy.Field()