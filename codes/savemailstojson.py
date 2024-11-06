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

def remove_emojis(text):
    # Pattern Unicode pour détecter les emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticônes
        "\U0001F300-\U0001F5FF"  # symboles et pictogrammes divers
        "\U0001F680-\U0001F6FF"  # transport et symboles
        "\U0001F700-\U0001F77F"  # symboles alchimiques
        "\U0001F780-\U0001F7FF"  # symboles géométriques
        "\U0001F800-\U0001F8FF"  # symboles divers et pictogrammes
        "\U0001F900-\U0001F9FF"  # émoticônes supplémentaires et autres
        "\U0001FA00-\U0001FA6F"  # objets divers
        "\U00002702-\U000027B0"  # divers
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub(r'', text)

def save_email_to_file(email_data, filename="codes/mails.json"):
    # Charger les emails existants s'ils existent avec un encodage utf-8
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
                email_list = existing_data.get("emails", [])  # Récupérer la liste des emails
        except UnicodeDecodeError:
            # Si l'encodage utf-8 échoue, tenter avec un autre encodage
            with open(filename, 'r', encoding='cp1252', errors='ignore') as file:
                existing_data = json.load(file)
                email_list = existing_data.get("emails", [])  # Récupérer la liste des emails
    else:
        email_list = []

    # Appliquer le nettoyage des URLs, emojis, et autres caractères à chaque email
    for email in email_data:
        if "body" in email:
            email["body"] = clean_all_urls(email["body"])
            email["body"] = remove_emojis(email["body"])

    # Ajouter les nouveaux emails nettoyés à la liste
    email_list.extend(email_data)

    # Créer le dictionnaire à enregistrer
    data_to_save = {
        "emails": email_list
    }

    # Enregistrer dans le fichier JSON avec un encodage utf-8
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data_to_save, file, ensure_ascii=False, indent=4)

    print(f"{len(email_data)} emails saved to {filename}")