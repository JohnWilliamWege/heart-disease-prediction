import pandas as pd
from database.connection import create_connection, close_connection
from database.schema import create_table


# Loading CSV into DataFrame
csv_file = 'C:/Users/jwweg/PycharmProjects/heart_disease_app/heart.csv'
db_file = 'C:/Users/jwweg/PycharmProjects/heart_disease_app/patients.db'


def check_data_exists(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM patients")
    count = cursor.fetchone()[0]
    return count > 0



def load_csv_to_db(csv_file, db_file):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file, delimiter=';')
        print("CSV file loaded successfully.")

        # set up a connection to the SQLite database
        conn = create_connection(db_file)
        if conn is None:
            raise Exception("Error! cannot create the database connection.")
        print("Database connection created successfully.")

        # create the table if not exists
        create_table(conn)

        # Check if data already exists
        if not check_data_exists(conn):

            df.to_sql('patients', conn, if_exists='append', index=False)
            print("Data inserted successfully.")
        else:
            print("Data already exists in the database. No new data was added.")


        close_connection(conn)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    load_csv_to_db(csv_file, db_file)
