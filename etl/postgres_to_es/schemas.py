from typing import Optional
from pydantic import BaseModel


class FilmWorkSchema(BaseModel):
    id: str
    imdb_rating: Optional[float]
    title: str
    description: Optional[str]
    genres: list[str] = []
    actors_names: list[str] = []
    writers_names: list[str] = []
    directors_names: list[str] = []
    actors: list[dict] = []
    writers: list[dict] = []
    directors: list[dict] = []
