import scrapy


class Music(scrapy.Item):
    link = scrapy.Field()
    duration = scrapy.Field()
    title = scrapy.Field()
    genre = scrapy.Field()


class MusicLink(scrapy.Item):
    genre = scrapy.Field()
    link = scrapy.Field()
