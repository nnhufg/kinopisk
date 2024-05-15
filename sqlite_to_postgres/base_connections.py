import logging
import os
import sqlite3
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor

from load_data import main

sqlite_db_path = 'db.sqlite'

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="error.log"
)


dsn = {
    'dbname': 'movies_database',
    'user': 'app',
    'password': '123qwe',
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


def set_connections():
    pg_conn = None
    try:
        with sqlite_connection(sqlite_db_path) as sqlite_conn, psycopg2.connect(
            **dsn, cursor_factory=DictCursor
        ) as pg_conn:
            main(sqlite_conn, pg_conn)
    except (sqlite3.Error, psycopg2.Error) as _e:
        logging.error("\nОшибка: %s", _e)
        print(f'\n{_e}\n')
    finally:
        if pg_conn is not None:
            pg_conn.close()
