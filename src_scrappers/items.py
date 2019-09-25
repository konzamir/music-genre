import scrapy


class Music(scrapy.Item):
    download_link = scrapy.Field()
    duration = scrapy.Field()
    name = scrapy.Field()
    id = scrapy.Field()


class MusicLink(scrapy.Item):
    genre = scrapy.Field()
    link = scrapy.Field()


class ParsedUrl(scrapy.Item):
    url = scrapy.Field()
    genre = scrapy.Field()
