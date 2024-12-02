from mistralcognitionagent import agentclassification
from sendmails import authenticate_gmail, send_email
import json

from mistralcognitionagent import agentclassification
from sendmails import authenticate_gmail, send_email
import json

# Fonction pour récupérer l'adresse e-mail authentifiée
def get_authenticated_email():
    """
    Récupère l'adresse e-mail de l'utilisateur authentifié à partir du service Gmail.
    """
    try:
        # Créer un service Gmail avec l'authentification existante
        service = authenticate_gmail()
        
        # Obtenir les informations du profil de l'utilisateur
        user_profile = service.users().getProfile(userId='me').execute()
        email_address = user_profile.get('emailAddress')
        return email_address
    except Exception as e:
        print(f"Failed to retrieve authenticated email: {e}")
        return None

# Étape 1 : Charger les emails fictifs pour la reconnaissance
def test_recognition_with_recipients():
    print("Step 1: Testing recognition with recipients...")
    emails_file = 'codes/test_mails.json'  # Fichier contenant les emails de test
    recipients_file = 'codes/mailsdestinataires.json'  # Fichier contenant les destinataires
    results = []

    try:
        # Charger les emails fictifs
        with open(emails_file, 'r', encoding='utf-8') as file:
            test_emails = json.load(file)["emails"]

        # Charger les destinataires
        with open(recipients_file, 'r', encoding='utf-8') as file:
            recipients = json.load(file)["recipients"]

        # Créer une correspondance entre les fonctions et les emails des destinataires
        recipient_map = {recipient["fonction"].lower(): recipient["email"] for recipient in recipients}

        # Reconnaissance et correspondance des emails
        for mail in test_emails:
            try:
                subject_body = f"Subject: {mail['subject']}\nBody: {mail['body']}"
                keywords, subject = agentclassification(subject_body)
                
                # Vérifier les résultats de classification
                if not keywords or not subject:
                    print(f"Skipping email '{mail['subject']}' due to incomplete classification.")
                    continue

                # Normaliser le sujet pour la correspondance avec les destinataires
                subject = subject.lower()

                # Associer le résultat de reconnaissance à un destinataire
                recipient_email = recipient_map.get(subject)
                if recipient_email:
                    results.append((mail['subject'], subject, keywords, recipient_email))
                    print(f"'{mail['subject']}' classified as '{subject}' with keywords '{keywords}', sending to {recipient_email}.")
                else:
                    print(f"No recipient found for classification subject: '{subject}'.")
            except Exception as e:
                print(f"Error processing email '{mail.get('subject', 'Unknown')}': {e}")

    except Exception as e:
        print(f"Error during recognition or loading files: {e}")
    return results

# Étape 2 : Envoyer les résultats de reconnaissance aux destinataires
def send_recognition_results_with_recipients(results):
    print("Step 2: Sending recognition results via email...")
    # Authentification Gmail
    service = authenticate_gmail()
    if not service:
        print("Failed to authenticate Gmail. Exiting.")
        return

    # Récupérer l'email authentifié
    sender_email = get_authenticated_email()
    if not sender_email:
        print("Could not retrieve the authenticated sender email. Exiting.")
        return

    # Envoyer un email pour chaque résultat
    for subject, classification_result, keywords, recipient_email in results:
        subject_email = f"Results for '{subject}'"
        body = (
            f"Hello,\n\n"
            f"The email with subject: '{subject}'\n"
            f"was classified as: '{classification_result}'.\n"
            f"Keywords: {keywords}\n\n"
            f"Best regards,\nAutomated System"
        )

        try:
            send_email(service, sender_email, recipient_email, subject_email, body)
            print(f"Email sent to {recipient_email} for classification '{classification_result}'.")
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")

# Tester la reconnaissance et l'envoi des emails
if __name__ == "__main__":
    recognition_results = test_recognition_with_recipients()
    if recognition_results:
        send_recognition_results_with_recipients(recognition_results)
    else:
        print("No recognition results to send.")
