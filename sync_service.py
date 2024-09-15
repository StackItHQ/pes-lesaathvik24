import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google_sheets_helper import connect_to_google_sheet, get_data_from_sheet, update_sheet_data_in_batches, delete_rows_in_sheet
from mysql_helper import connect_to_mysql, get_data_from_mysql, update_mysql_data_in_batches, delete_rows_in_mysql


class SyncHandler(FileSystemEventHandler):
    def __init__(self, sheet_id, worksheet_name, mysql_table, batch_size=100):
        self.worksheet = connect_to_google_sheet(sheet_id, worksheet_name)
        self.conn = connect_to_mysql()
        self.cursor = self.conn.cursor()
        self.mysql_table = mysql_table
        self.batch_size = batch_size

    def sync_sheet_to_db(self):
        """Sync data from Google Sheets to MySQL and only update changed rows."""
        sheet_data = get_data_from_sheet(self.worksheet)
        db_data = get_data_from_mysql(self.cursor, self.mysql_table)

        # Detect deleted rows in Google Sheets
        deleted_rows = db_data[~db_data.index.isin(sheet_data.index)]
        if not deleted_rows.empty:
            delete_rows_in_mysql(self.cursor, self.mysql_table, deleted_rows)
            self.conn.commit()

        # Sync only the updated rows from Google Sheets to MySQL
        changed_rows = sheet_data[sheet_data.ne(db_data).any(axis=1)]
        if not changed_rows.empty:
            update_mysql_data_in_batches(
                self.cursor, self.mysql_table, changed_rows, self.batch_size)
            self.conn.commit()

    def sync_db_to_sheet(self):
        """Sync data from MySQL to Google Sheets and only update changed rows."""
        db_data = get_data_from_mysql(self.cursor, self.mysql_table)
        sheet_data = get_data_from_sheet(self.worksheet)

        # Detect deleted rows in MySQL
        deleted_rows = sheet_data[~sheet_data.index.isin(db_data.index)]
        if not deleted_rows.empty:
            delete_rows_in_sheet(self.worksheet, deleted_rows)

        # Sync only the updated rows from MySQL to Google Sheets
        changed_rows = db_data[db_data.ne(sheet_data).any(axis=1)]
        if not changed_rows.empty:
            update_sheet_data_in_batches(
                self.worksheet, changed_rows, self.batch_size)

    def start_sync(self):
        """Sync data between Google Sheets and MySQL."""
        self.sync_db_to_sheet()
        self.sync_sheet_to_db()


def run_sync_service(sheet_id, worksheet_name, mysql_table, batch_size=100, sync_interval=10):
    handler = SyncHandler(sheet_id, worksheet_name,
                          mysql_table, batch_size=batch_size)
    observer = Observer()
    observer.schedule(handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(sync_interval)  # Sync every sync_interval seconds
            handler.start_sync()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
