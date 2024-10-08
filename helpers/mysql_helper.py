import mysql.connector
import pandas as pd


def connect_to_mysql():
    """Establish connection to MySQL database."""
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Iluvaudi$24",
        database="sync_db"
    )


def get_data_from_mysql(cursor, table_name):
    """Fetch data from MySQL table."""
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    return pd.DataFrame(rows, columns=columns)


def update_mysql_data_in_batches(cursor, table_name, data, batch_size=100):
    """Update the MySQL table with data from Google Sheets in batches, only updating changed rows."""
    data_chunks = process_data_in_batches(data, batch_size)

    for chunk in data_chunks:
        for row in chunk.itertuples(index=False):
            update_query = f"REPLACE INTO {table_name} VALUES ({','.join(['%s'] * len(data.columns))})"
            cursor.execute(update_query, row)


def delete_rows_in_mysql(cursor, table_name, deleted_rows):
    """Delete rows in MySQL based on deleted rows in Google Sheets."""
    for index, row in deleted_rows.iterrows():
        # Assuming 'id' is the primary key
        delete_query = f"DELETE FROM {table_name} WHERE id = %s"
        cursor.execute(delete_query, (row['id'],))


def process_data_in_batches(data, batch_size=100):
    """Helper function to split data into batches."""
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]
