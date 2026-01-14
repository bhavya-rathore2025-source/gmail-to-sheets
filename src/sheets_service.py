# src/sheets_service.py

import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from config import SCOPES, CREDENTIALS_PATH, TOKEN_PATH


def get_sheets_service():
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(
            TOKEN_PATH, SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("OAuth token missing. Run Gmail auth first.")

    service = build("sheets", "v4", credentials=creds)
    return service

def get_existing_message_ids(service, spreadsheet_id, sheet_name):
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A2:A"
    ).execute()

    values = result.get("values", [])
    return {row[0] for row in values if row}

def append_email_row(service, spreadsheet_id, sheet_name, email):
    values = [[
        email["message_id"],
        email["from"],
        email["subject"],
        email["date"],
        email["content"]
    ]]

    body = {"values": values}

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
