import os
import json
import re

def clean_all_urls(text):
    # Suppression des sauts de ligne et autres caractères d'échappement
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    # Suppression des espaces multiples par un seul espace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Regex pour capturer toutes les URLs dans le texte
    pattern = r"(https?://[^\s]+|www\.[^\s]+|mailto:[^\s]+)"
    
    # Remplacer toutes les URLs par leur forme texte (non cliquable)
    text = re.sub(pattern, r'\g<0>', text)  # Remplace par le texte de l'URL lui-même
    
    return text.strip()

def save_email_to_file(email_data, filename="codes/mails.json"):
    # Charger les emails existants s'ils existent
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
            email_list = existing_data.get("emails", [])  # Récupérer la liste des emails
    else:
        email_list = []

    # Appliquer le nettoyage des URLs et autres caractères à chaque email
    for email in email_data:
        if "body" in email:
            email["body"] = clean_all_urls(email["body"])

    # Ajouter les nouveaux emails nettoyés à la liste
    email_list.extend(email_data)

    # Créer le dictionnaire à enregistrer
    data_to_save = {
        "emails": email_list
    }

    # Enregistrer dans le fichier JSON
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data_to_save, file, ensure_ascii=False, indent=4)

    print(f"{len(email_data)} emails saved to {filename}")
