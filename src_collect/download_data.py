import asyncio
import os

from db_connect import DBConn
from fetch_data import FetchData

from settings import PACK_LIMIT


class DownloadData:
    sleep_time = 1
    curr_id = 0

    offset = 0

    def __init__(self):
        last_id = 0
        if not os.path.isfile('logs/current.log'):
            with open('logs/current.log', 'r') as f:
                line = f.readline()
                if line:
                   last_id = int(line)
        self.curr_id = last_id

    async def _get_data(self):
        data = DBConn.get_data_from_table(
            table='music',
            where={
                'download_link': ['is', 'not', 'NULL'],
                'id': ['>', self.curr_id]
            },
            limit=PACK_LIMIT,
            offset=self.offset,
            table_fields=[
                'id', 'download_link', 'genre', 'duration'
            ]
        )
        self.offset += PACK_LIMIT
        return data

    async def _fetch_data(self):
        data = await self._get_data()

        while data:
            yield data
            data = await self._get_data()

    async def _download_link(self, ob):
        path = f"../dataset/{ob['genre']}"
        FetchData.collect(path=path, file=f"{ob['id']}.mp3", url=ob['download_link'])

    async def _download_pack(self, iter):
        id = iter[0]['id']
        for music in iter:
            await self._download_link(ob=music)
            id = music['id']

        return id

    async def run(self):
        async for iter in self._fetch_data():
            id = await self._download_pack(iter)

            with open('logs/current.log', 'w+') as f:
                f.write(str(id))
