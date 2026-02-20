BOT_NAME = 'flo_crawler'

SPIDER_MODULES = ['flo_crawler.spiders']
NEWSPIDER_MODULE = 'flo_crawler.spiders'

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 2

ITEM_PIPELINES = {
    'flo_crawler.pipelines.FloCrawlerPipeline': 300,
}

REQUEST_FINGERTIP_ENABLED = False

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'