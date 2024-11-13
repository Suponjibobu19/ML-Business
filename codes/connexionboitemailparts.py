import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.compose']

def readEmailsPart():
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
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])
        
        if not messages:
            print('No new messages.')
        else:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                
                # Extract email headers for subject, sender, and date
                email_data = msg['payload']['headers']
                subject = None
                from_name = None
                date = None
                for header in email_data:
                    if header['name'] == 'Subject':
                        subject = header['value']
                    if header['name'] == 'From':
                        from_name = header['value']
                    if header['name'] == 'Date':
                        date = header['value']
                
                # Print the subject, sender, and date
                print(f"From: {from_name}")
                print(f"Subject: {subject}")
                print(f"Date: {date}")
                
                # Extract and decode the plain text body
                body = ""
                if 'parts' in msg['payload']:
                    for part in msg['payload']['parts']:
                        if part['mimeType'] == 'text/plain':
                            data = part['body']["data"]
                            byte_code = base64.urlsafe_b64decode(data)
                            body += byte_code.decode("utf-8")
                
                # Print the plain text body
                print("Message Body:", body)
                
                # Mark the message as read
                service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
    
    except Exception as error:
        print(f'An error occurred: {error}')

# Call the function to read emails
readEmailsPart()
