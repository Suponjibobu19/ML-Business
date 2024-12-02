import json
from mistralcognitionagent import agentclassification

def load_recipients(filename):
    """
    Charge les destinataires depuis un fichier JSON.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            recipients = json.load(file)["recipients"]
            return {rec["fonction"].lower(): rec["email"] for rec in recipients}
    except Exception as e:
        print(f"Error loading recipients: {e}")
        return {}

def associate_predictions_with_recipients(emails, recipients_file):
    """
    Associate predictions with recipients based on email classification.
    """
    recipients = load_recipients(recipients_file)
    classification_results = []

    for email in emails:
        try:
            subject_body = f"Subject: {email['subject']}\nBody: {email['body']}"
            keywords, subject = agentclassification(subject_body)

            recipient_email = recipients.get(subject.lower(), None)
            if recipient_email:
                classification_results.append({
                    "email_id": email["email_id"],
                    "from": email["from"],
                    "email_subject": email["subject"],
                    "email_body": email["body"],
                    "classified_as": subject,
                    "recipient_email": recipient_email,
                })
                print(f"Email '{email['subject']}' classified as '{subject}' and assigned to {recipient_email}.")
            else:
                print(f"Warning: No recipient found for classification '{subject}'.")
        except Exception as e:
            print(f"Error processing email '{email['subject']}': {e}")

    return classification_results


