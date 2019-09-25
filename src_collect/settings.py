import os
import sys

from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path=dotenv_path)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")

DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASS}@"\
    f"{DB_HOST}:{'3306'}/{DB_NAME}"

PACK_LIMIT = int(os.getenv("PACK_LIMIT"))
