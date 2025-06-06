import psycopg2
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = psycopg2.connect(
    dbname="poker",
    user="postgres",
    password="postgres",
    host="host.docker.internal",
    port=5432
    )
    try:
        yield conn
    finally:
        conn.close()