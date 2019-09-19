from items import MusicLink, Music


class SrcPipeline(object):
    def process_item(self, item, spider):
        # spider.logger.info(item)
        if isinstance(item, MusicLink):
            self.save_music_link(item)
        if isinstance(item, Music):
            self.save_music_item(item)
        return item

    def save_music_item(self, item):
        pass

    def save_music_link(self, item):
        pass
