from dataclasses import astuple
import sqlite3
from psycopg2.extensions import connection as _connection
from base_dataclasses import FilmWork, Genre, Person, GenreFilmwork, PersonFilmwork


class SQLiteExtractor:

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def copy_from_film_work(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM film_work;")

        result = cursor.fetchall()

        films = [FilmWork(**dict(film_work)) for film_work in result]

        return films

    def copy_from_genre(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM genre;")

        result = cursor.fetchall()

        genres = [Genre(**dict(genre)) for genre in result]

        return genres

    def copy_from_person(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM person;")

        result = cursor.fetchall()

        persons = [Person(**dict(person)) for person in result]

        return persons

    def copy_from_genre_film_work(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM genre_film_work;")

        result = cursor.fetchall()

        genre_film_works = [
            GenreFilmwork(**dict(genre_film_work)) for genre_film_work in result
        ]

        return genre_film_works

    def copy_from_person_film_work(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM person_film_work;")

        result = cursor.fetchall()

        person_film_works = [
            PersonFilmwork(
                **{
                    key: value
                    for key, value in dict(person_film_work).items()
                    if key != "id"
                }
            )
            for person_film_work in result
        ]

        return person_film_works

    def extract_all(self):
        films = self.copy_from_film_work()
        genres = self.copy_from_genre()
        persons = self.copy_from_person()
        genre_film_works = self.copy_from_genre_film_work()
        person_film_works = self.copy_from_person_film_work()

        return films, genres, persons, genre_film_works, person_film_works


class PostgresSaver:

    def __init__(self, pg_conn: _connection):
        self.pg_conn = pg_conn

    def save_film_work_to_postgres(self, films: list):

        print("\n[PROCCESS]: Начинаю загрузку фильмов...\n")
        with self.pg_conn.cursor() as cursor:
            cursor.execute(
                f"SELECT column_name FROM information_schema.columns WHERE table_name = 'film_work' ORDER BY ordinal_position;"
            )
            column_names_list = [row[0] for row in cursor.fetchall()]
            column_names_str = ",".join(column_names_list)

            col_count = ", ".join(["%s"] * len(column_names_list))
            bind_values = ",".join(
                cursor.mogrify(f"({col_count})", astuple(film)).decode("utf-8")
                for film in films
            )

            cursor.execute(
                f"""INSERT INTO content.film_work ({column_names_str}) VALUES {bind_values} ON CONFLICT DO NOTHING """
            )
            print(f"\nЗагрузка окончена!\n")

    def save_genre_to_postgres(self, genres: list):

        print("\n[PROCCESS]: Начинаю загрузку жанров...\n")
        with self.pg_conn.cursor() as cursor:
            cursor.execute(
                f"SELECT column_name FROM information_schema.columns WHERE table_name = 'genre' ORDER BY ordinal_position;"
            )
            column_names_list = [row[0] for row in cursor.fetchall()]
            column_names_str = ",".join(column_names_list)

            col_count = ", ".join(["%s"] * len(column_names_list))
            bind_values = ",".join(
                cursor.mogrify(f"({col_count})", astuple(genre)).decode("utf-8")
                for genre in genres
            )

            cursor.execute(
                f"""INSERT INTO content.genre ({column_names_str}) VALUES {bind_values} ON CONFLICT DO NOTHING """
            )
            print(f"\nЗагрузка окончена!\n")

    def save_persons_to_postgres(self, persons: list):

        print("\n[PROCCESS]: Начинаю загрузку актёров...\n")
        with self.pg_conn.cursor() as cursor:
            cursor.execute(
                f"SELECT column_name FROM information_schema.columns WHERE table_name = 'person' ORDER BY ordinal_position;"
            )
            column_names_list = [row[0] for row in cursor.fetchall()]
            column_names_str = ",".join(column_names_list)

            col_count = ", ".join(["%s"] * len(column_names_list))
            bind_values = ",".join(
                cursor.mogrify(f"({col_count})", astuple(person)).decode("utf-8")
                for person in persons
            )

            cursor.execute(
                f"""INSERT INTO content.person ({column_names_str}) VALUES {bind_values} ON CONFLICT DO NOTHING """
            )
            print(f"\nЗагрузка окончена!\n")

    def save_genre_film_work_to_postgres(self, genre_film_works: list):

        print(
            "\n[PROCCESS]: Начинаю загрузку промежуточной таблицы фильмы - жанры...\n"
        )
        with self.pg_conn.cursor() as cursor:
            cursor.execute(
                f"SELECT column_name FROM information_schema.columns WHERE table_name = 'genre_film_work' ORDER BY ordinal_position;"
            )
            column_names_list = [row[0] for row in cursor.fetchall()]
            column_names_str = ",".join(column_names_list)

            col_count = ", ".join(["%s"] * len(column_names_list))
            bind_values = ",".join(
                cursor.mogrify(f"({col_count})", astuple(genre_film_work)).decode(
                    "utf-8"
                )
                for genre_film_work in genre_film_works
            )

            cursor.execute(
                f"""INSERT INTO content.genre_film_work ({column_names_str}) VALUES {bind_values} ON CONFLICT DO NOTHING"""
            )
            print(f"\nЗагрузка окончена!\n")

    def save_person_film_work_to_postgres(self, person_film_works: list):

        print("\n[PROCCESS]: Начинаю загрузку промеуточно таблицы фильмы - люди...\n")
        with self.pg_conn.cursor() as cursor:
            cursor.execute(
                f"SELECT column_name FROM information_schema.columns WHERE table_name = 'person_film_work' ORDER BY ordinal_position;"
            )
            column_names_list = [row[0] for row in cursor.fetchall()]
            column_names_str = ",".join(column_names_list)
            col_count = ", ".join(["%s"] * len(column_names_list))
            bind_values = ",".join(
                cursor.mogrify(f"({col_count})", astuple(person_film_work)).decode(
                    "utf-8"
                )
                for person_film_work in person_film_works
            )

            cursor.execute(
                f"""INSERT INTO content.person_film_work ({column_names_str}) VALUES {bind_values} ON CONFLICT DO NOTHING"""
            )
            print(f"\nЗагрузка окончена!\n")

    def save_data_to_postgres(self, table_name: str, data: list):
        print(f"\n[PROCCESS]: Начинаю загрузку данных в таблицу {table_name}...\n")
        with self.pg_conn.cursor() as cursor:
            cursor.execute(
                f"SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position;",
                (table_name,),
            )
            column_names_list = [row[0] for row in cursor.fetchall()]
            column_names_str = ",".join(column_names_list)

            col_count = ", ".join(["%s"] * len(column_names_list))
            bind_values = ",".join(
                cursor.mogrify(f"({col_count})", astuple(row)).decode("utf-8")
                for row in data
            )

            cursor.execute(
                f"INSERT INTO content.{table_name} ({column_names_str}) VALUES {bind_values} ON CONFLICT DO NOTHING"
            )

            print(f"\nЗагрузка данных в таблицу {table_name} завершена!\n")
