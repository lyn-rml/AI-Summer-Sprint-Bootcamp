import json
import os

DB_FILE = "emails.json"

def save_email(email_data):
    emails = get_all_emails()
    emails.append(email_data)
    with open(DB_FILE, "w") as f:
        json.dump(emails, f, indent=4)

def get_all_emails():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)
