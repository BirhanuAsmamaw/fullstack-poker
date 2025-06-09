import os
import psycopg2
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = psycopg2.connect(
        dbname=os.environ.get("POSTGRES_DB", "poker"),
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=os.environ.get("POSTGRES_PASSWORD", "postgres"),
        host=os.environ.get("POSTGRES_HOST", "host.docker.internal"),
        port=os.environ.get("POSTGRES_PORT", 5432),
    )
    try:
        yield conn
    finally:
        conn.close()
