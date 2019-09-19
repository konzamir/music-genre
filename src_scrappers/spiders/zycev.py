# -*- coding: utf-8 -*-
import scrapy

from items import MusicLink


class ZaycevSpider(scrapy.Spider):
    name = 'zaycev'

    def start_requests(self):
        # yield scrapy.http.Request(
        #     url='https://zaycev.net/genres/index.html',
        #     callback=self.parse
        # )
        # yield scrapy.http.Request(
        #     url='https://zaycev.net/pages/45824/4582412.shtml',
        #     callback=self.parse_song
        # )
        yield scrapy.http.Request(
            url='http://zaycev.net/genres/pop/index_7036.html',
            callback=self.parse_genre
        )

    def parse(self, response):
        genres = response.xpath(
            '//ul[contains(@class, "genre__filter")]/li/a')
        for genre in genres:
            genre_url = genre.xpath('./@href').get()
            genre_text = genre.xpath('./text()').get('')

            if genre_url:
                url = response.urljoin(genre_url)
                yield scrapy.http.Request(
                    url=url,
                    meta={
                        'genre': genre_text
                    },
                    callback=self.parse_genre
                )

    def parse_genre(self, response):
        url = response.url
        genre_start_pos = url.find('genres') + len('genres') + 1
        genre_end_pos = url.find('/', genre_start_pos)
        genre = url[genre_start_pos:genre_end_pos]

        url_next_page = response.xpath(
            '//a[contains(@class, "pager__item_last")]/@href').get()
        url_next_page = response.urljoin(url_next_page)

        if url_next_page and url_next_page is not response.url:
            yield scrapy.http.Request(
                url=url_next_page,
                callback=self.parse_genre
            )

        try:
            for req in self.parse_music_list(response, genre):
                yield req
        except TypeError:
            self.logger.info('Music urls from page were fetched!')

    def parse_music_list(self, response, genre):
        music_list = response.xpath(
            '//div[contains(@class, "musicset-track-list__items")]'
            '/div[contains(@class, "musicset-track")]')
        for music in music_list:
            music_block_class = music.xpath('./@class').get('')
            if music_block_class.find('track-is-banned') == -1 and music_block_class:
                data_key = music.xpath('./@data-dkey').get()
                data_key = data_key[:data_key.find('.')]

                music_url = f'/pages{data_key}.shtml'
                music_url = response.urljoin(music_url)

                item = MusicLink()
                item['link'] = music_url
                item['genre'] = genre
                yield item

                # yield scrapy.http.Request(
                #     url=music_url,
                #     callback=self.parse_song,
                #     meta={
                #         'genre': genre
                #     }
                # )
