from src.gmail_service import get_gmail_service, fetch_unread_emails
from src.email_parser import parse_email

if __name__ == "__main__":
    service = get_gmail_service()
    messages = fetch_unread_emails(service)

    print(f"Fetched {len(messages)} unread emails")

    for msg in messages:
        email = parse_email(service, msg["id"])
        print("\n--- EMAIL ---")
        print(email)
