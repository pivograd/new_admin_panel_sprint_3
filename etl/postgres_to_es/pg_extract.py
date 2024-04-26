import psycopg2
import logging
from backoff import backoff
from psycopg2.extensions import connection as _connection

logger = logging.getLogger(__name__)


class PostgresExtractor:
    """
    Класс для получения данных из PostgreSQL
    """

    @backoff()
    def __init__(self, pg_conn: _connection, chunk: int = 100):
        self.connection = pg_conn
        self.chunk = chunk

    @backoff()
    def extract_data(self, last_modified: tuple):
        try:
            with self.connection.cursor() as curs:
                curs.execute(
                    f"""SELECT
                fw.id,
                fw.title,
                fw.description,
                fw.rating,
                fw.type,
                fw.created,
                fw.modified,
                COALESCE (
                    json_agg(
                        DISTINCT jsonb_build_object(
                            'person_role', pfw.role,
                            'person_id', p.id,
                            'person_name', p.full_name
                        )
                    ) FILTER (WHERE p.id is not null),
                    '[]'
                ) as persons,
                COALESCE(
                    json_agg(
                        DISTINCT g.name
                        ) FILTER (WHERE g.id IS NOT NULL),
                        '[]'
                    ) AS genres
                FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                WHERE fw.modified > %s OR p.modified > %s OR g.modified > %s
                GROUP BY fw.id""", last_modified)

                while data := curs.fetchmany(self.chunk):
                    yield data

        except psycopg2.Error as e:
            logger.error(e)
            return
