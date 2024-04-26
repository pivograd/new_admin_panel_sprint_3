import json
import logging

from backoff import backoff
from elasticsearch import Elasticsearch, helpers

logger = logging.getLogger(__name__)


class ESLoader(Elasticsearch):
    """
    Класс для загрузки подготовленных данных в elasticsearch
    """

    def __init__(self, host, index_name):
        super(ESLoader, self).__init__(hosts=host)
        self.create_index(index_name)

    @backoff()
    def create_index(self, index_name):
        if not self.indices.exists(index=index_name):
            index_settings = json.loads(open(
                'index_settings.json').read())
            self.indices.create(index=index_name, body=index_settings)

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
        transform_data = self.transform_data_for_load(data)
        helpers.bulk(self, transform_data)
