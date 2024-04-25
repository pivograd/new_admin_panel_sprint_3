import json
import logging

from backoff import backoff
from elasticsearch import Elasticsearch, helpers

logger = logging.getLogger(__name__)


class ESLoader(Elasticsearch):
    """
    Класс для загрузки подготовленных данных в elasticsearch
    """

    def __init__(self, host):
        super(ESLoader, self).__init__(hosts=host)

    def create_index(self):
        if not self.indices.exists(index='movies'):
            index_settings = json.loads(open(
                'index_settings.json').read())
            self.indices.create(index='movies', body=index_settings)

    @staticmethod
    def transform_data_for_load(data):
        transform_data = [
            {
                "_index": 'movies',
                "_id": document.id,
                "_source": document.json()
            }
            for document in data
        ]

        return transform_data

    @backoff()
    def load_es_data(self, data):
        self.create_index()
        transform_data = self.transform_data_for_load(data)
        helpers.bulk(self, transform_data)
