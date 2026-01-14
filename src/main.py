# src/main.py

import logging
import time

from src.gmail_service import (
    get_gmail_service,
    fetch_unread_emails,
    mark_as_read,
)
from src.email_parser import parse_email
from src.sheets_service import (
    get_sheets_service,
    get_existing_message_ids,
    append_email_row,
)

# ---------- CONFIG ----------
SPREADSHEET_ID = "1SYtPDjQ_5b2SUwQq0RCawn5SF3ug9LT8z2FcuJ5bU3A"
SHEET_NAME = "Sheet1"
ENABLE_SUBJECT_FILTER = False
SUBJECT_KEYWORD = "invoice"

# ---------- LOGGING ----------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

#--Retry Logic----
def retry(func, retries=3, delay=2):
    for attempt in range(0, retries):
        try:
            return func()
        except Exception as e:
            logging.warning(
                f"Retry {attempt}/{retries} failed: {e}"
            )
            if attempt == retries:
                raise
            time.sleep(delay)

# ---------- MAIN ----------
def main():
    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service()

    messages = fetch_unread_emails(gmail_service)
    logging.info(f"Fetched {len(messages)} unread emails")

    existing_ids = get_existing_message_ids(
        sheets_service, SPREADSHEET_ID, SHEET_NAME
    )

    for msg in messages:
        message_id = msg["id"]

        # Duplicate check
        if message_id in existing_ids:
            logging.info(f"Skipping duplicate message {message_id}")
            continue

        email = parse_email(gmail_service, message_id)

        # Optional subject filter
        if ENABLE_SUBJECT_FILTER:
            if SUBJECT_KEYWORD.lower() not in email["subject"].lower():
                logging.info(f"Skipping non-matching subject: {email['subject']}")
                continue


        # Append to Sheet
        retry(lambda: append_email_row(
        sheets_service, SPREADSHEET_ID, SHEET_NAME, email))
        logging.info(f"Stored message {message_id} in sheet")

        # Mark as read
        retry(lambda: mark_as_read(gmail_service, message_id))
        logging.info(f"Read message {message_id}")

    logging.info("Run completed successfully")


if __name__ == "__main__":
    main()
