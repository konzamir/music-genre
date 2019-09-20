import asyncio
from download_data import DownloadData


if __name__ == '__main__':
    app = DownloadData()
    asyncio.run(app.run())

