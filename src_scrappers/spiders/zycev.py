import scrapy

from items import MusicLink, ParsedUrl

from glob import glob


class ZaycevSpider(scrapy.Spider):
    name = 'zaycev'

    def start_requests(self):
        logs = glob('./logs/*.*')
        paths = []
        is_valid = True

        for path in logs:
            if path.find('.gitignore') == -1:
                with open(path, 'r') as file:
                    data = file.readline()
                    if not data:
                        is_valid = False
                    paths.append(data)

        if is_valid and len(paths) == 16:
            for url in paths:
                yield scrapy.http.Request(
                    url=url,
                    callback=self.parse_genre
                )
        else:
            yield scrapy.http.Request(
                url='https://zaycev.net/genres/index.html',
                callback=self.parse
            )

    def _get_genre(self, url):
        genre_start_pos = url.find('genres') + len('genres') + 1
        genre_end_pos = url.find('/', genre_start_pos)
        genre = url[genre_start_pos:genre_end_pos]

        return genre

    def parse(self, response):
        genres = response.xpath(
            '//ul[contains(@class, "genre__filter")]/li/a')
        pages = []

        for genre in genres:
            genre_url = genre.xpath('./@href').get()
            if genre_url:
                url = response.urljoin(genre_url)
                genre = self._get_genre(url)

                item = ParsedUrl()
                item['url'] = url
                item['genre'] = genre

                pages.append(url)
                yield item

        for url in pages:
            yield scrapy.http.Request(
                url=url,
                callback=self.parse_genre
            )

    def parse_genre(self, response):
        url = response.url
        genre = self._get_genre(url)

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

        item = ParsedUrl()
        item['url'] = response.url
        item['genre'] = genre
        yield item

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
