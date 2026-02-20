import pymongo

class FloCrawlerPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['flo_monitoring']
        self.collection = self.db['prices']

    def process_item(self, item, spider):
        self.collection.update_one(
            {'product_id': item['product_id']},
            {
                '$set': {
                    'brand': item['brand'],
                    'model': item['model'],
                    'url': item['url'],
                    'last_updated': item['timestamp']
                },
                '$push': {
                    'price_history': {
                        'price': item['price'],
                        'date': item['timestamp']
                    }
                }
            },
            upsert=True
        )
        return item