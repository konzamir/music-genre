from db_connect import DBConn
from fetch_data import FetchData

from settings import PACK_LIMIT


class DownloadData:
    sleep_time = 1

    def _get_data(self):
        data = DBConn.get_data_from_table(
            table='music',
            where={
                'download_link': ['is', 'not', 'NULL']
            },
            limit=PACK_LIMIT,
            table_fields=[
                'id', 'download_link', 'genre', 'duration'
            ]
        )
        return data

    def _fetch_data(self):
        data = self._get_data()

        while data:
            yield data
            data = self._get_data()

    def _download_link(self, ob):
        path = f"../dataset/{ob['genre']}"
        FetchData.collect(path=path, file=f"{ob['id']}.mp3", url=ob['download_link'])

    def run(self):
        for iter in self._fetch_data():
            for music in iter:
                self._download_link(ob=music)

            print('=' * 50)
            print(f'Pack was downloded! Sleep for {self.sleep_time} sec...')
            print('=' * 50)
