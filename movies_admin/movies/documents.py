from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text


class FilmWorkDocument(Document):
    title = Text()
    description = Text()

    class Index:
        name = 'film'
