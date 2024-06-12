import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)

        print(f"Connected to SQLite Database version: {sqlite3.version}")

    except Error as error:
        print(error)

    return conn


def close_connection(conn):
    try:
        conn.close()
        print("Connection closed")

    except Error as error:
        print(error)