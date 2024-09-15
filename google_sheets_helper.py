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


def update_sheet_data_in_batches(worksheet, new_data, batch_size=100):
    """Update only changed rows in Google Sheets in batches."""
    current_data = get_data_from_sheet(worksheet)

    # Break new data into chunks for processing in batches
    new_data_chunks = process_data_in_batches(new_data, batch_size)

    for chunk in new_data_chunks:
        for idx, row in chunk.iterrows():
            if idx >= len(current_data) or not row.equals(current_data.iloc[idx]):
                # Adjust the column range as needed
                range_to_update = f'A{idx+2}:E{idx+2}'
                worksheet.update(range_to_update, [row.values.tolist()])


def process_data_in_batches(data, batch_size=100):
    """Helper function to split data into batches."""
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]
