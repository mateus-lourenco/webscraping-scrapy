from letras.items import Genero
import pymongo

class LetrasPipeline(object):

    collection_name = 'musicas_mpb'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'letras_db')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, Genero):
            instance = self.db.musicas.find_one({"titulo": item["titulo"], "artista": item["artista"]}) 
            if not instance:
                self.db[self.collection_name].insert_one(dict(item))

        return item