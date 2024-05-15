import psycopg2
import sqlite3
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from psycopg2.extensions import connection as _connection
import os


sqlite_db_path = os.environ.get('DB_PATH')


dsn = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
    'options': os.environ.get('DB_OPTIONS'),
}


@contextmanager
def sqlite_connection(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def databases_connections():
    pg_conn = None
    try:
        with sqlite_connection(sqlite_db_path) as sqlite_conn, psycopg2.connect(
            **dsn, cursor_factory=DictCursor
        ) as pg_conn:
            main_databases(sqlite_conn, pg_conn)
    except (sqlite3.Error, psycopg2.Error) as _e:
        print("\nОшибка:", _e)
    finally:
        if pg_conn is not None:
            pg_conn.close()


def main_databases(connection: sqlite3.Connection, pg_conn: _connection):

    base_class = BasesChecker(connection, pg_conn)

    try:
        base_class.check_amount()
    except psycopg2.IntegrityError as _e:
        print(f"\n[ERROR]: {_e}\n")


class BasesChecker:

    def __init__(self, sql_conn: sqlite3.Connection, pg_conn: _connection):
        self.sql_conn = sql_conn
        self.pg_conn = pg_conn
        
    
    def check_amount(self):

        tables = ['film_work', 'genre', 'person', 'genre_film_work', 'person_film_work']
        sql_cursor = self.sql_conn.cursor()
        postgre_cursor = self.pg_conn.cursor()

        for table in tables:
            sql_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            sqlite_count = sql_cursor.fetchone()[0]

            postgre_cursor.execute(f"SELECT COUNT(*) FROM content.{table}")
            postgresql_count = postgre_cursor.fetchone()[0]

            try:
                assert sqlite_count == postgresql_count, f"Count mismatch for table '{table}': SQLite has {sqlite_count} records, PostgreSQL has {postgresql_count} records"
            except AssertionError as _e:
                print(f"\nНедостаток значений в таблицах!\n[ERROR]: {_e}\n")
            





if __name__ == '__main__':
    databases_connections()