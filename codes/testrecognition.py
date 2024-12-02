from mistralcognitionagent import agentclassification
import json
6
# Chemin vers le fichier JSON contenant les emails de test
jsonfile = 'codes/test_mails.json'

# Charger les emails de test depuis le fichier JSON
with open(jsonfile, 'r', encoding='utf-8') as file:
    data = json.load(file)
    for mail in data['emails']:
        try:
            # Crée une chaîne de texte avec seulement le sujet et le contenu
            subject_body = f"Subject: {mail['subject']}\nBody: {mail['body']}"
            
            # Appeler la fonction de reconnaissance
            keywords, subject = agentclassification(subject_body)
            
            # Vérifier et afficher les résultats
            if keywords and subject:
                print(f"Email: {mail['subject']}")
                print(f"Keywords: {keywords}")
                print(f"Predicted Subject: {subject}")
                print("-" * 50)
            else:
                print(f"Failed to classify email: {mail['subject']}")
                print("-" * 50)

        except Exception as e:
            print(f"An error occurred while processing email '{mail['subject']}': {e}")
            print("-" * 50)
