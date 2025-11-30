import sqlite3
from typing import Annotated

from fastapi import Depends

from app.config import db_path, schema_path


def get_db():
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def get_db_conn():
    conn = get_db()
    try:
        yield conn
    finally:
        conn.close()


DBConnDep = Annotated[sqlite3.Connection, Depends(get_db_conn)]


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    try:
        with open(schema_path, "r") as f:
            cursor.executescript(f.read())
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Warning: Could not initialize database from schema.sql: {e}")