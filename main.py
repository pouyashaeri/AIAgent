# main.py

import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from requests import Request

# Load secrets from .env
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

# If modifying these SCOPES, delete the token.json file.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    if os.path.exists('creds/token.json'):
        creds = Credentials.from_authorized_user_file('creds/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('creds/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('creds/token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = SENDER_EMAIL
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email(to, subject, body):
    service = get_gmail_service()
    message = create_message(to, subject, body)
    sent = service.users().messages().send(userId="me", body=message).execute()
    print("Message sent! Message ID:", sent['id'])

if __name__ == "__main__":
    # Simple test
    send_email("pouyashaeri@gmail.com", "Test Email", "Hello from your AI Agent!")
