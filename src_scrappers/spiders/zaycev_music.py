# -*- coding: utf-8 -*-
import scrapy

from items import Music
from handlers import DBHandler


class ZaycevMusicSpider(scrapy.Spider):
    name = 'zaycev_music'
    offset = 0
    pack_limit = 50

    def _get_data(self):
        data = DBHandler.get_data_from_table(
            table='music',
            where={
                'status': ['is', 'NULL', 'or', 'status', '=', '0']
            },
            limit=self.pack_limit,
            offset=self.offset
        )

        self.offset += self.pack_limit

        return data

    def start_requests(self):
        d = self._get_data()
        ids = []
        for music in d:
            url = music['link']
            yield scrapy.http.Request(
                url=url,
                callback=self.parse,
                meta={
                    'id': music['id']
                }
            )
            ids.append(music['id'])

        ids = ', '.join([str(x) for x in ids])
        ids = f"({ids})"
        DBHandler.update_table_data(
            table='music',
            where={
                'id': ['in', ids]
            },
            data={
                'status': 1
            }
        )

    def parse(self, response):
        link = response.xpath(
            '//a[contains(@class, "button-download__link")]/@href').get()

        if link:
            link = link[::-1]
            link_end_pos = link.find('/')
            link = link[link_end_pos:]
            link = link[::-1]
            link = f"{link}{response.meta.get('id', 0)}.mp3"

        duration = response.xpath(
            '//div[contains(@class, "musicset-track")]/@data-duration').get()
        title = response.xpath(
            '//div[contains(@class, "musicset-track")]/@title').get()

        music_item = Music()
        music_item['download_link'] = link
        music_item['duration'] = duration
        music_item['name'] = title
        music_item['id'] = response.meta.get('id')
        yield music_item

        # for req in self.start_urls():
        #     yield req
