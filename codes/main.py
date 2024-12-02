from returnmails import returnEmails
from savemailstojson import save_email_to_file
from mistralcognitionagent import agentclassification
from sendmails import authenticate_gmail, send_email, get_authenticated_email
from associate_recipients import load_recipients

# Charger les destinataires globalement
recipient_map = {}

def load_recipient_map():
    """
    Charge les destinataires et crée un dictionnaire global.
    """
    global recipient_map
    try:
        recipient_map = load_recipients("codes/mailsdestinataires.json")
        print("Recipient map loaded successfully.")
    except Exception as e:
        print(f"Error loading recipient map: {e}")


def step_1_retrieve_emails():
    print("Step 1: Retrieving emails...")
    try:
        emails = returnEmails()
        if emails:
            print(f"Retrieved {len(emails)} emails.")
            for email in emails:
                print(f"Email ID: {email['email_id']}, From: {email['from']}, Subject: {email['subject']}")
        return emails
    except Exception as e:
        print(f"Error retrieving emails: {e}")
        return []


def step_2_save_emails(emails):
    print("Step 2: Saving emails...")
    try:
        save_email_to_file(emails)
        print("Emails saved successfully.")
    except Exception as e:
        print(f"Error saving emails: {e}")


def step_3_classify_emails(emails):
    print("Step 3: Classifying emails...")
    global recipient_map
    classification_results = []

    if not recipient_map:
        print("Recipient map is empty. Please load it first.")
        return []

    try:
        for email in emails:
            subject_body = f"Subject: {email['subject']}\nBody: {email['body']}"
            try:
                keywords, subject = agentclassification(subject_body)
                recipient_email = recipient_map.get(subject.lower())

                if recipient_email:
                    classification_results.append({
                        "email_id": email["email_id"],
                        "from": email["from"],
                        "email_subject": email["subject"],
                        "email_body": email["body"],
                        "classified_as": subject,
                        "recipient_email": recipient_email,
                    })
                    print(f"Classified '{email['subject']}' as '{subject}' -> Recipient: {recipient_email}")
                else:
                    print(f"No recipient found for classification '{subject}'.")
            except Exception as e:
                print(f"Error classifying email '{email['subject']}': {e}")
    except Exception as e:
        print(f"Error during classification: {e}")

    return classification_results


def step_4_send_emails(classification_results):
    print("Step 4: Sending emails...")
    try:
        sender_email = get_authenticated_email()
        if not sender_email:
            raise ValueError("Authenticated sender email not found.")

        service = authenticate_gmail()

        for result in classification_results:
            subject = f"Processed Email: {result['email_subject']}"
            body = (
                f"Hello,\n\n"
                f"The following email was processed:\n\n"
                f"Email ID: {result['email_id']}\n"
                f"From: {result['from']}\n"
                f"Subject: {result['email_subject']}\n"
                f"Body: {result['email_body']}\n\n"
                f"Classification: {result['classified_as']}\n\n"
                f"Best regards,\nAutomated System"
            )
            recipient_email = result["recipient_email"]

            try:
                send_email(service, sender_email, recipient_email, subject, body)
                print(f"Email sent to {recipient_email} for subject '{result['email_subject']}'.")
            except Exception as e:
                print(f"Error sending email to {recipient_email}: {e}")
    except Exception as e:
        print(f"Error during email sending: {e}")


if __name__ == "__main__":
    print("Starting the automated email process...")
    try:
        load_recipient_map()

        emails = step_1_retrieve_emails()
        if not emails:
            print("No emails retrieved. Exiting.")
            exit()

        step_2_save_emails(emails)
        classified_emails = step_3_classify_emails(emails)

        if classified_emails:
            step_4_send_emails(classified_emails)
        else:
            print("No emails classified. Skipping email sending.")

        print("Process completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
