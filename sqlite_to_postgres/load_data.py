import sqlite3
import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection as _connection
from base_dataclasses import *
from extractors_savers import *
from base_connections import *

psycopg2.extras.register_uuid()


def main(connection: sqlite3.Connection, pg_conn: _connection):

    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    data_dictionary = {
        'film_work': sqlite_extractor.copy_from_film_work,
        'genre': sqlite_extractor.copy_from_genre,
        'person': sqlite_extractor.copy_from_person,
        'genre_film_work': sqlite_extractor.copy_from_genre_film_work,
        'person_film_work': sqlite_extractor.copy_from_person_film_work
    }

    try:
        for table_name, extractor_func in data_dictionary.items():
            data = extractor_func()
            postgres_saver.save_data_to_postgres(table_name, data)
    except psycopg2.IntegrityError as _e:
        print(f"\n[HINT]: Не забудь добавить обработку конфликта в SQL.\nОбнаружен дубликат ключа. Пропускаем запись...\n\n[ERROR]: {_e}\n")


if __name__ == '__main__':
    set_connections()
