# src/main.py

from src.gmail_service import get_gmail_service, fetch_unread_emails


if __name__ == "__main__":
    service = get_gmail_service()
    messages = fetch_unread_emails(service)
    print(f"Fetched {len(messages)} unread emails")
