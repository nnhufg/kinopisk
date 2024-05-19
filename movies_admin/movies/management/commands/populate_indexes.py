import redis
import logging
from typing import Any
from django.core.management.base import BaseCommand
from movies.models import Filmwork
from movies.documents import FilmWorkDocument
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class Command(BaseCommand):
    help = 'Перенос данных из PostgreSQL в Elasticsearch'

    def handle(self, *args: Any, **options: Any) -> str | None:

        logger = logging.getLogger(__name__)

        client = Elasticsearch('http://elasticsearch:9200', request_timeout=10)
        rs = redis.Redis(host='redis', port=6379, decode_responses=True)

        index_name = 'movies'
        
        body = {
            "settings": {
                "refresh_interval": "1s",
                "analysis": {
                    "filter": {
                        "english_stop": {
                            "type": "stop",
                            "stopwords": "_english_"
                        },
                        "english_stemmer": {
                            "type": "stemmer",
                            "language": "english"
                        },
                        "english_possessive_stemmer": {
                            "type": "stemmer",
                            "language": "possessive_english"
                        },
                        "russian_stop": {
                            "type": "stop",
                            "stopwords": "_russian_"
                        },
                        "russian_stemmer": {
                            "type": "stemmer",
                            "language": "russian"
                        }
                    },
                    "analyzer": {
                        "ru_en": {
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "english_stop",
                                "english_stemmer",
                                "english_possessive_stemmer",
                                "russian_stop",
                                "russian_stemmer"
                            ]
                        }
                    }
                }
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "imdb_rating": {"type": "float"},
                    "genres": {"type": "keyword"},
                    "title": {
                        "type": "text",
                        "analyzer": "ru_en",
                        "fields": {"raw": {"type": "keyword"}}
                    },
                    "description": {"type": "text", "analyzer": "ru_en"},
                    "directors_names": {"type": "text", "analyzer": "ru_en"},
                    "actors_names": {"type": "text", "analyzer": "ru_en"},
                    "writers_names": {"type": "text", "analyzer": "ru_en"},
                    "directors": {
                        "type": "nested",
                        "dynamic": "strict",
                        "properties": {
                            "id": {"type": "keyword"},
                            "name": {"type": "text", "analyzer": "ru_en"}
                        }
                    },
                    "actors": {
                        "type": "nested",
                        "dynamic": "strict",
                        "properties": {
                            "id": {"type": "keyword"},
                            "name": {"type": "text", "analyzer": "ru_en"}
                        }
                    },
                    "writers": {
                        "type": "nested",
                        "dynamic": "strict",
                        "properties": {
                            "id": {"type": "keyword"},
                            "name": {"type": "text", "analyzer": "ru_en"}
                        }
                    }
                }
            }
        } 

        try:
            if not client.indices.exists(index=index_name):
                client.indices.create(index=index_name, body=body)
                logger.info('\nИндекс успешно создан!\n')
            else:
                logger.warning('\nИндекс уже существует!\n')
        except Exception as _e:
            logger.error(f'\nОшибка: {_e}\n')
        

        last_processed_id = rs.get('id')
        if last_processed_id is not None:
            last_processed_id = int(last_processed_id)
        else:
            last_processed_id = 0

        bulk_data = []

        try:
            for film in Filmwork.objects.filter(id__gt=last_processed_id):
                # сохраняем текущее состояние в redis
                rs.set('id', str(film.id))
                # получаем текущее состояние из redis и проверяем его
                value =  rs.get('id')
                if value == str(film.id):
                    bulk_data.append({
                        '_op_type': 'index', # указываем операцию
                        '_index': index_name, # указываем в какой индекс помещать документы
                        '_id': str(film.id), # обязательно приводим id к строке
                        '_source': { # указываем документ для помещения в индекс
                            'title': film.title, 
                            'description': film.description
                        }
                    })
            logger.info('\nФильмы успешно добавлены в массив!\n')
        except Exception as _e:
            logger.error(f'\nОшибка: {_e}\n')
        finally:
            rs.delete('id')
            logger.info('\nКэш очищен!\n')

        try:
            bulk(client, bulk_data) # запускаем операцию c bulk
            self.stdout.write(self.style.SUCCESS('\nДанные успешно проиндексированы!\n'))
        except Exception as _e:
            logger.error(f'\nОшибка при выполнении bulk: {_e}\n')

        
