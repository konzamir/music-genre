import os
import requests


class FetchData:
    @classmethod
    def _get_data(cls, url):
        print('+' * 50)
        print(f'Downloading link: {url}...')
        r = requests.get(url)

        print(f'Finished with code {r.status_code}!')
        print('+' * 50)

        return r.content

    @classmethod
    def _check_dir(cls, path):
        if not os.path.isdir(path):
            print("Dir is empty, creating...")
            os.mkdir(path)
        print("Dir is exists")

    @classmethod
    def _save_data(cls, path, file, content):
        cls._check_dir(path)

        full_file_path = os.path.join(path, file)
        with open(full_file_path, "wb") as f:
            f.write(content)

    @classmethod
    def collect(cls, path, file, url, *a, **kw):
        content = cls._get_data(url)
        cls._save_data(path=path, file=file, content=content)
