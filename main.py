from sync_service import run_sync_service
import gspread
if __name__ == "__main__":
    SHEET_ID = "1dG8_Z0kPGlWuPzgYQFH9xhZ1OEW3BJMw4X3NLosHPyY"
    WORKSHEET_NAME = "Class Data"
    MYSQL_TABLE = "sync_table"

    run_sync_service(SHEET_ID, WORKSHEET_NAME, MYSQL_TABLE)
