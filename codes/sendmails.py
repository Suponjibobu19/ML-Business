import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

# Scopes pour lire et envoyer des emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


# Fonction pour créer le message MIME
def create_message(sender, to, subject, message_text):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = to
    message['Subject'] = subject
    message.attach(MIMEText(message_text, 'plain'))
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

# Fonction pour envoyer un email via l'API Gmail
def send_email(service, sender, to, subject, message_text):
    message = create_message(sender, to, subject, message_text)
    try:
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        print(f"Message sent to {to}, Message Id: {sent_message['id']}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Charger les destinataires depuis un fichier JSON
def load_recipients(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data['recipients']
    except Exception as e:
        print(f"Error loading recipients: {e}")
        return []

# Envoi des emails à partir de la liste des destinataires
def send_emails_to_recipients(service, sender, filename, subject, body):
    recipients = load_recipients(filename)
    for recipient in recipients:
        email_address = recipient.get("email")
        if email_address:
            send_email(service, sender, email_address, subject, body)
        else:
            print(f"No valid email address for recipient: {recipient}")

# Utilisation du script pour envoyer un email
if __name__ == "__main__":
    # Authentifier l'utilisateur et créer le service Gmail
    service = authenticate_gmail()

    # Définir l'expéditeur, le sujet et le corps du message
    sender_email = "your_email@gmail.com"
    subject = "Notification"
    body = "This is a test email sent from the automated system."

    # Envoyer les emails
    send_emails_to_recipients(service, sender_email, "codes/addresses.json", subject, body)
