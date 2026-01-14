## Name: BHAVYA PRATAP SINGH Rathore

## LinkedIn: https://www.linkedin.com/in/bhavyapratap98/

## Introduction

This project is a Python-based automation system that integrates the **Gmail API** and **Google Sheets API** to read real incoming emails and store them in a Google Sheet.

The application processes **only unread emails**, extracts relevant information such as sender, subject, date, and content, and appends the data as structured rows in Google Sheets. To ensure safe re-runs, the system prevents duplicate entries and marks emails as read after successful processing.

The project demonstrates secure API usage with OAuth 2.0, clean code structure, state persistence, and reliable automation design.

---

## Code Structure & Function Responsibilities

The project follows a modular structure where each file has a clear and single responsibility.

- `gmail_service.py` – Handles Gmail API authentication, fetching unread emails, and marking emails as read.

- `email_parser.py` – Parses raw Gmail messages and extracts sender, subject, date, and email content.

- `sheets_service.py` – Manages Google Sheets API interactions, duplicate prevention, and appending rows.

- `main.py` – Orchestrates the complete workflow and integrates all services.

- `config.py` – Stores configuration values such as API scopes and file paths.

## High-Level Architecture Diagram

The simple diagram below shows the data flow of the application.

Gmail Inbox (Unread Emails)
↓
Gmail API (OAuth 2.0)
↓
Python Application

    	-Fetch unread email message IDs

    	-Load existing messageIds from Google Sheet

    	-Skip duplicate emails

    	-Parse non-duplicate emails

    	-Apply subject filter (If filter on)

↓
Google Sheets API
↓
Append Email to Google Sheets (Auto-Retry on Failure)
↓
Emails marked as READ (Auto-Retry on Failure)

This architecture ensures

-> duplicate emails are skipped
-> Optional Subject based filtering
-> Retry on failure instead of crashing

## Setup Instructions

Follow the steps below to set up and run the project locally.

---

### Step 1: Download the Project

1. Click on Code → Download ZIP from the repository
2. Extract the ZIP file
3. Open the extracted folder in VS Code

---

### Step 2: Create and Activate Virtual Environment

Run the following commands in the terminal:

python -m venv .venv
.venv\Scripts\activate (Windows)

---

### Step 3: Install Dependencies

Run:

pip install -r requirements.txt

---

### Step 4: Google Cloud Configuration

1. Create a Google Cloud project
2. Enable Gmail API and Google Sheets API
3. Configure OAuth Consent Screen (External)
4. Create OAuth Client ID (Desktop Application)
5. Download credentials.json and place it inside the credentials/ folder

---

### Step 5: Prepare Google Sheet

1. Create a new Google Sheet
2. Add the following header row:

messageId | From | Subject | Date | Content

3. Copy the Spreadsheet ID from the Google Sheet URL
4. Paste it into main.py:

SPREADSHEET_ID = "your_spreadsheet_id_here"

---

### Step 6: Run the Application

Run:

python -m src.main

- First run opens OAuth consent screen
- Grant access to Gmail and Google Sheets
- Token is saved locally for future runs

---

### Step 7: Re-run Safety Check

- Re-running the script does not create duplicate rows
- Already processed emails are skipped
- Emails are marked as read after successful processing

## Design Explanation

### OAuth Flow Used

The application uses **OAuth 2.0 (Desktop Application flow)** to securely access Gmail and Google Sheets on behalf of the user.

On the first run, the script opens a browser window where the user grants permission to access their Gmail inbox and Google Sheets. After successful authorization, Google issues an access token and a refresh token, which are stored locally in `token.json`.

On subsequent runs, the stored token is reused and refreshed automatically if expired, so the user is not required to log in again. No passwords or API keys are stored in the code, ensuring secure authentication.

---

### Duplicate Prevention Logic

To prevent duplicate rows in Google Sheets, the application uses the **Gmail message ID** as a unique identifier for each email.

Before inserting new data, the script reads all existing message IDs from the Google Sheet and loads them into a Python `set`. Since set lookups are fast and unique by nature, the script can efficiently check whether an email has already been processed.

If the message ID already exists, the email is skipped. This makes the script safe to re-run multiple times without creating duplicate entries.

---

### State Persistence Method

The application uses the **Google Sheet itself as persistent state**.

Each processed email’s `messageId` is stored in the first column of the sheet. On every execution, the script reads these stored IDs to determine which emails have already been processed.

This approach avoids the need for an external state file and ensures that state is preserved across script restarts, system reboots, and multiple executions. It also makes the state easy to inspect and debug directly from the spreadsheet.

## Challenges Faced & Solution

### OAuth Scope Mismatch Causing API Access Failure

While integrating Google Sheets, the application returned a **403 “insufficient authentication scopes”** error even though Gmail access was working correctly.

**Cause:**  
The OAuth token was initially generated with **Gmail-only scope**. OAuth tokens cannot be extended after creation, so the same token failed when attempting to access the Google Sheets API.

**Solution:**  
I updated the configuration to use **combined Gmail and Google Sheets scopes**, deleted the existing OAuth token, and re-authorized the application. This regenerated a token with all required permissions.

**Result:**  
Both Gmail and Google Sheets APIs worked correctly using a single OAuth flow, and the script executed end-to-end without errors.

## Limitations

- The Google Sheet structure (header row and column order) is assumed to be **pre-created** to avoid accidental schema changes.
- Emails are filtered based on a **simple subject keyword match**, more advanced filtering rules are not implemented.
- Html to Plain text Bonus not implemented
- The solution is designed for **small to medium inbox volumes** and is not optimized for very large mailboxes.
