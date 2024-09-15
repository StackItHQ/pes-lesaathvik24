import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


def connect_to_google_sheet(sheet_id, worksheet_name):
    """Connect to Google Sheets and return the worksheet."""
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)
    return worksheet


def is_sync_paused(worksheet):
    """Check if sync is paused based on the value in cell A1."""
    sync_status = worksheet.acell(
        'A1').value  # Assuming A1 holds 'PAUSE' or 'RUN'
    return sync_status.strip().upper() == "PAUSE"


def get_data_from_sheet(worksheet):
    """Fetch data from Google Sheets."""
    data = worksheet.get_all_values()
    return pd.DataFrame(data[1:], columns=data[0])


def update_sheet_data(worksheet, new_data):
    """Update only changed rows in Google Sheets."""
    current_data = get_data_from_sheet(worksheet)

    # Convert all Timestamp columns to strings
    new_data = new_data.applymap(lambda x: str(
        x) if isinstance(x, pd.Timestamp) else x)
    current_data = current_data.applymap(
        lambda x: str(x) if isinstance(x, pd.Timestamp) else x)

    # Update only rows that are different
    for idx, row in new_data.iterrows():
        if idx >= len(current_data) or not row.equals(current_data.iloc[idx]):
            # Adjust the column range as needed
            range_to_update = f'A{idx+2}:E{idx+2}'
            worksheet.update(range_to_update, [row.values.tolist()])
