import hashlib
from items import MusicLink, Music, ParsedUrl

from handlers import DBHandler


class SrcPipeline(object):
    def process_item(self, item, spider):
        # spider.logger.info(item)
        if isinstance(item, MusicLink):
            self.save_music_link(item)
        if isinstance(item, Music):
            self.save_music_item(item)
        if isinstance(item, ParsedUrl):
            self.save_parsed_link(item)
        return item

    def save_parsed_link(self, item):
        with open(f"logs/{item['genre']}.log", 'w+') as file:
            file.write(item['url'])

    def save_music_item(self, item):
        pass

    def save_music_link(self, item):
        store_data = dict(item)
        store_data['hash_link'] = hashlib.md5(store_data['link'].encode()).hexdigest()

        DBHandler.insert_into_table(table='music', data=store_data)
