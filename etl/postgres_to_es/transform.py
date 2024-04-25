from backoff import backoff
from schemas import FilmWorkSchema


class Transformer:
    """
    Класс для преобразования данных в подходящий для elasticsearch формат
    """

    @staticmethod
    def distribution_by_roles(all_persons: list[dict]):
        roles = ('director', 'actor', 'writer')
        persons_by_role = {}
        for role in roles:
            persons_by_role[role] = [[], []]
        for person in all_persons:
            person_info = {'id': person['person_id'], 'name': person['person_name']}
            persons_by_role[person['person_role']][0].append(person_info)
            persons_by_role[person['person_role']][1].append(person['person_name'])

        return persons_by_role

    def transform_data(self, data: list[dict]):
        es_data = []
        for data_object in data:
            persons = self.distribution_by_roles(data_object['persons'])
            film_work = FilmWorkSchema(
                id=data_object['id'],
                imdb_rating=data_object['rating'],
                genres=data_object['genres'],
                title=data_object['title'],
                description=data_object['description'],
                directors_names=persons['director'][1],
                actors_names=persons['actor'][1],
                writers_names=persons['writer'][1],
                directors=persons['director'][0],
                actors=persons['actor'][0],
                writers=persons['writer'][0],
            )

            es_data.append(film_work)

        return es_data
