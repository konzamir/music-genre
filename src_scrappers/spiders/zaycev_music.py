# -*- coding: utf-8 -*-
import scrapy

from items import Music


class ZaycevMusicSpider(scrapy.Spider):
    name = 'zaycev_music'

    def start_requests(self):
        pass

    def parse(self, response):
        genre = response.meta.get('genre')

        link = response.xpath(
            '//a[contains(@class, "button-download__link")]/@href').get()

        if link:
            link = link[::-1]
            link_end_pos = link.find('/')
            link = link[link_end_pos:]
            link = link[::-1]
            link = link + '{}.mp3'

            duration = response.xpath(
                '//div[contains(@class, "musicset-track")]/@data-duration').get()
            title = response.xpath(
                '//div[contains(@class, "musicset-track")]/@title').get()

            music_item = Music()
            music_item['link'] = link
            music_item['duration'] = duration
            music_item['title'] = title
            music_item['genre'] = genre
            yield music_item
