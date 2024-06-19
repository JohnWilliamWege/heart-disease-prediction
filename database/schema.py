import sqlite3
from sqlite3 import Error
from database.connection import create_connection
from database.connection import close_connection

db_file = "C:/Users/jwweg/PycharmProjects/heart_disease_app/patients.db"


def create_table(conn):

    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER NOT NULL,
                sex INTEGER NOT NULL,
                cp INTEGER NOT NULL,
                trestbps INTEGER NOT NULL,
                chol INTEGER NOT NULL,
                fbs INTEGER NOT NULL,
                restecg INTEGER NOT NULL,
                thalach INTEGER NOT NULL,
                exang INTEGER NOT NULL,
                oldpeak REAL NOT NULL,
                slope INTEGER NOT NULL,
                ca INTEGER NOT NULL,
                thal INTEGER NOT NULL,
                target INTEGER NOT NULL
            );
        """)
        conn.commit()
        print("Table has been created successfully.")
    except Error as error:
        print("Failed to create table:", error)


def main():

    conn = create_connection(db_file)
    if conn is not None:
        create_table(conn)

        close_connection(conn)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()


def check_data_exists(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM patients")
    count = cursor.fetchone()[0]
    return count > 0
