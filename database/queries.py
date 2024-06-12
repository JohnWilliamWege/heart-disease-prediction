from connection import create_connection, close_connection
import sqlite3
from sqlite3 import Error

db_file = "C:/Users/jwweg/PycharmProjects/heart_disease_app/patients.db"

def check_table_contents(db_file):

    try:
        conn = create_connection(db_file)

        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

            close_connection(conn)
        else:
            print("Error! cannot create the database connection.")
    except Error as error:
        print(error)


check_table_contents(db_file)
