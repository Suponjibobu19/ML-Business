from mistralai import Mistral

import time

def agentclassification(query):
    """
    Analyse le texte et retourne les mots-clés et la matière prédite.
    """
    try:
        api_key = "S1pZGonHlgCIFMUzm3Y6O5jShDbJegMl"
        client = Mistral(api_key=api_key)

        prompt = (
            f"Je veux que tu identifies le mot clé principal ou un ensemble de mots-clés qui permettent d'identifier "
            f"le service ou la personne qui devrait recevoir cet email et que tu me dises à qui envoyer le mail.\n\n"
            f"Je veux que tu me répondes avec 2 strings, une pour les mots clés et une pour la prédiction de la matière "
            f"parmi la liste suivante :\n\n"
            f"- Advanced Data Analysis and Visualization\n"
            f"- AI and Data Science for Marketing\n"
            f"- AI Clinic\n"
            f"- Career Coatching\n"
            f"- Data Anonymization\n"
            f"- Deep Learning Computer Vision\n"
            f"- Deep Learning: Methods and Applications\n"
            f"- Deployment and Maintenance of AI Models\n"
            f"- English\n"
            f"- Explainable AI\n"
            f"- Fair Machine Learning\n"
            f"- Machine Learning: Business Project\n"
            f"- Natural Language Processing\n"
            f"- Supply Chain Management and Smart Operations\n"
            f"- Venture Capital\n\n"
            f"Réponds en minuscule, aucune majuscule, voici la forme exacte de la réponse :\n\n"
            f"\"Keywords: <list of keywords>\"\n"
            f"\"Subject: <subject area>\"\n\n"
            f"Texte à analyser :\n\n{query}"
        )

        response = client.agents.complete(
            agent_id="ag:becb4bf0:20241012:redirection:8e1c095d",
            messages=[{"role": "user", "content": prompt}],
        )
        result = response.choices[0].message.content

        # Log de la réponse brute
        print(f"Raw response: {result}")

        # Parsing amélioré pour extraire les mots-clés et la matière
        keywords = None
        subject = None
        for line in result.splitlines():
            line = line.strip().strip('"')  # Enlever les guillemets et les espaces
            if line.lower().startswith("keywords:"):
                keywords = line.split(":", 1)[1].strip()
            elif line.lower().startswith("subject:"):
                subject = line.split(":", 1)[1].strip()

        if not keywords or not subject:
            raise ValueError("Mistral returned an incomplete response.")

        return keywords, subject

    except Exception as e:
        print(f"Error during classification: {e}")
        return None, None
