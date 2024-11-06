from mistralcognitionagent import agentclassification
import json

jsonfile = 'codes\\mails.json'

with open(jsonfile, 'r', encoding='utf-8') as file:
    data = json.load(file)
    for mail in data['emails']:
        # Crée une chaîne de texte avec seulement le sujet et le contenu
        subject_body = f"Subject: {mail['subject']}\nBody: {mail['body']}"
        agentclassification(subject_body)
