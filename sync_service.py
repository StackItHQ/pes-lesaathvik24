import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google_sheets_helper import connect_to_google_sheet, get_data_from_sheet, update_sheet_data
from mysql_helper import connect_to_mysql, get_data_from_mysql, update_mysql_data


class SyncHandler(FileSystemEventHandler):
    def __init__(self, sheet_id, worksheet_name, mysql_table):
        self.worksheet = connect_to_google_sheet(sheet_id, worksheet_name)
        self.conn = connect_to_mysql()
        self.cursor = self.conn.cursor()
        self.mysql_table = mysql_table

    def sync_sheet_to_db(self):
        sheet_data = get_data_from_sheet(self.worksheet)
        db_data = get_data_from_mysql(self.cursor, self.mysql_table)
        if not sheet_data.equals(db_data):
            update_mysql_data(self.cursor, self.mysql_table, sheet_data)
            self.conn.commit()

    def sync_db_to_sheet(self):
        db_data = get_data_from_mysql(self.cursor, self.mysql_table)
        sheet_data = get_data_from_sheet(self.worksheet)
        if not db_data.equals(sheet_data):
            update_sheet_data(self.worksheet, db_data)

    def on_modified(self, event):
        if event.src_path.endswith('.json'):  
            self.sync_sheet_to_db()

    def start_sync(self):
        self.sync_sheet_to_db()
        self.sync_db_to_sheet()


def run_sync_service(sheet_id, worksheet_name, mysql_table):
    handler = SyncHandler(sheet_id, worksheet_name, mysql_table)
    observer = Observer()
    observer.schedule(handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
            handler.start_sync()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
