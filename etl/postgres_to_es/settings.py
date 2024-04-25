import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
logging.basicConfig(level=logging.INFO, filename=os.path.join(BASE_DIR, 'postgres_to_es/py_log.log'),
                    filemode="w", format="%(asctime)s %(levelname)s %(message)s")

DSL = {'dbname': os.environ.get('POSTGRES_DB'),
       'user': os.environ.get('POSTGRES_USER'),
       'password': os.environ.get('POSTGRES_PASSWORD'),
       'host': 'postgres',
       'port': 5432}

INDEX_NAME = 'movies'

ES_HOST = os.environ.get("ES_HOST", "http://127.0.0.1:9200")
FILE_PATH = os.environ.get("FILE_PATH", "state.json")
