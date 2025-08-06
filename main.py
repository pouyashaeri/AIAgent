import os
import base64
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from PyPDF2 import PdfReader

from utils import generate_followup_email, log_interaction

# ========== LOAD ENV ==========
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("TARGET_EMAIL")
JOB_URL = os.getenv("JOB_LINK")

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


# ========== GMAIL AUTH ==========

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


# ========== EMAIL CREATION ==========

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
    print("Email sent! Message ID:", sent['id'])


# ========== FETCH JOB DESCRIPTION ==========

def fetch_job_description(url, save_path="job_description.txt"):
    print(f"Fetching job description from: {url}")
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator='\n')
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Saved job description to {save_path}")
    except Exception as e:
        print(f"Failed to fetch job description: {e}")
        raise


# ========== FILE READERS ==========

def read_resume_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def read_job_description(txt_path):
    if not os.path.exists(txt_path):
        raise FileNotFoundError(f"Job description file not found: {txt_path}")
    with open(txt_path, 'r', encoding='utf-8') as file:
        return file.read()


# ========== MAIN ==========

if __name__ == "__main__":
    subject = "Follow-up: Student Researcher 2025 Application"

    fetch_job_description(JOB_URL)

    resume_text = read_resume_text("resume/resume.pdf")
    job_description = read_job_description("job_description.txt")

    print("Generating email using GPT-4...")
    email_body = generate_followup_email(resume_text, job_description, RECIPIENT_EMAIL)

    print("Sending email...")
    send_email(RECIPIENT_EMAIL, subject, email_body)

    print("Logging interaction...")
    log_interaction(RECIPIENT_EMAIL, "Student Researcher 2025", "SENT")

    print("Done!")
