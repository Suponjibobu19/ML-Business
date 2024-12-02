# sendmails.py
import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

# Scope for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    """
    Authenticates the user with the Gmail API and returns a service object.
    """
    creds = None

    if os.path.exists('codes/token.json'):
        creds = Credentials.from_authorized_user_file('codes/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('codes/my_cred_file.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('codes/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Error authenticating Gmail API: {e}")
        return None

def get_authenticated_email():
    """
    Retrieves the authenticated user's email address.
    """
    try:
        service = authenticate_gmail()
        user_profile = service.users().getProfile(userId='me').execute()
        return user_profile.get('emailAddress')
    except Exception as e:
        print(f"Failed to retrieve authenticated email: {e}")
        return None

def create_message(sender, to, subject, message_text):
    """
    Creates a MIME email message.
    """
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = to
    message['Subject'] = subject
    message.attach(MIMEText(message_text, 'plain'))
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email(service, sender, to, subject, message_text):
    """
    Sends an email via Gmail API.
    """
    message = create_message(sender, to, subject, message_text)
    try:
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        print(f"Email sent to {to}. Message ID: {sent_message['id']}")
    except Exception as e:
        print(f"Error sending email to {to}: {e}")

def send_emails_to_classified_recipients(service, classification_results):
    """
    Sends emails based on classification results.
    """
    sender = get_authenticated_email()
    if not sender:
        print("Failed to retrieve sender email. Aborting.")
        return

    for result in classification_results:
        recipient_email = result.get("recipient_email")
        if not recipient_email:
            print(f"Skipping email ID '{result.get('email_id')}' due to missing recipient email.")
            continue

        subject = f"Processed Email: {result.get('email_subject')}"
        body = (
            f"Hello,\n\n"
            f"The following email has been processed:\n\n"
            f"Email ID: {result.get('email_id')}\n"
            f"From: {result.get('from')}\n"
            f"Subject: {result.get('email_subject')}\n"
            f"Body: {result.get('email_body')}\n\n"
            f"Classification: {result.get('classified_as')}\n\n"
            f"Best regards,\nAutomated System"
        )

        try:
            send_email(service, sender, recipient_email, subject, body)
        except Exception as e:
            print(f"Error sending email to {recipient_email} for email ID '{result.get('email_id')}': {e}")
