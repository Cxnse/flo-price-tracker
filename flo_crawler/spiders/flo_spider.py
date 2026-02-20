import scrapy
import json
from ..items import FloCrawlerItem
from datetime import datetime


class FloSpider(scrapy.Spider):
    name = 'flo'
    start_urls = ['https://www.flo.com.tr/erkek?page=1']

    def parse(self, response):
        products = response.css('[data-gtm-product]')

        if not products:
            return

        for product in products:
            gtm_data = product.css('::attr(data-gtm-product)').get()

            if gtm_data:
                try:
                    data = json.loads(gtm_data)
                    item = FloCrawlerItem()

                    brand = data.get('brand')
                    if not brand:
                        brand = data.get('name', '').split()[0]
                    item['brand'] = brand

                    item['model'] = data.get('name', '')

                    sku = data.get('id') or data.get('sku')
                    item['product_id'] = str(sku)

                    price = data.get('price')
                    if price:
                        item['price'] = float(price)
                    else:
                        continue

                    link = product.css('a::attr(href)').get() or product.css('::attr(href)').get()
                    item['url'] = response.urljoin(link) if link else response.url

                    item['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    yield item

                except json.JSONDecodeError:
                    pass

        current_url = response.url
        if 'page=' in current_url:
            current_page = int(current_url.split('page=')[-1])
        else:
            current_page = 1

        next_page = current_page + 1
        next_url = f"https://www.flo.com.tr/erkek?page={next_page}"

        yield scrapy.Request(url=next_url, callback=self.parse)