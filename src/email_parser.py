import base64

def get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""


def decode_body(data):
    if not data:
        return ""

    decoded_bytes = base64.urlsafe_b64decode(data)
    return decoded_bytes.decode("utf-8", errors="ignore").strip()


def parse_email(service, message_id):
    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    email_data = {
        "from": get_header(headers, "From"),
        "subject": get_header(headers, "Subject"),
        "date": get_header(headers, "Date"),
        "content": ""
    }

    # Case 1: Simple email (no parts)
    if "data" in payload.get("body", {}):
        email_data["content"] = decode_body(payload["body"]["data"])

    # Case 2: Multipart email
    else:
        parts = payload.get("parts", [])
        for part in parts:
            if part.get("mimeType") == "text/plain":
                email_data["content"] = decode_body(
                    part["body"].get("data")
                )
                break

    return email_data
