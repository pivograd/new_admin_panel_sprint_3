import datetime
import logging
import time

import psycopg2

from settings import DSL, FILE_PATH, ES_HOST, INDEX_NAME
from psycopg2.extras import DictCursor
from pg_extract import PostgresExtractor
from transform import Transformer
from es_load import ESLoader
from state import JsonFileStorage, State

logger = logging.getLogger("ETl")

if __name__ == "__main__":
    es_loader = None
    pg_conn = None
    while True:
        try:
            with psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
                pg_extractor = PostgresExtractor(pg_conn)
                transformer = Transformer()
                es_loader = ESLoader(host=ES_HOST, index_name=INDEX_NAME)
                storage = JsonFileStorage(FILE_PATH)
                state = State(storage)

                last_modified = state.get_state('modified')
                if not last_modified:
                    last_modified = datetime.date.min.isoformat()
                    last_modified = (last_modified,) * 3
                else:
                    last_modified = (last_modified,) * 3
                data = pg_extractor.extract_data(last_modified)

                for data_chunk in data:
                    transform_data = transformer.transform_data(data_chunk)
                    try:
                        es_loader.load_es_data(transform_data)
                        state.set_state('modified', datetime.datetime.now().isoformat())
                        logger.info('Loaded: %s', transform_data)
                    except Exception as e:
                        logger.error('Failed: %s', e)

            time.sleep(100)

        except psycopg2.Error as e:
            logger.error(e)

        finally:
            if pg_conn:
                pg_conn.close()
            if es_loader:
                es_loader.transport.close()
