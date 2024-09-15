import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


def connect_to_google_sheet(sheet_id, worksheet_name):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)
    return worksheet


def get_data_from_sheet(worksheet):
    data = worksheet.get_all_values()
    return pd.DataFrame(data[1:], columns=data[0])


def update_sheet_data(worksheet, data):
    worksheet.clear()
    worksheet.update([data.columns.values.tolist()] + data.values.tolist())
