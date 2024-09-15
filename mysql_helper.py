import mysql.connector
import pandas as pd


def connect_to_mysql():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Iluvaudi$24",
        database="sync_db"
    )


def get_data_from_mysql(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    return pd.DataFrame(rows, columns=columns)


def update_mysql_data(cursor, table_name, data):
    """
    Update the MySQL table with the data from the Google Sheet.
    This clears the MySQL table and inserts new data based on the provided DataFrame.
    """
    cursor.execute(f"DELETE FROM {table_name}")  # Clear existing data

    # Insert updated data into MySQL
    for row in data.itertuples(index=False):
        cursor.execute(f"INSERT INTO {table_name} VALUES {tuple(row)}")
