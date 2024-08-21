import json
import torch
from transformers import pipeline
from tqdm import tqdm
from collections import Counter

"""
Description : Ce script analyse les abstracts de projets provenant d'un fichier JSON, les classifie dans différents domaines scientifiques
en utilisant un modèle de classification basé sur le langage naturel, et sauvegarde les résultats dans un fichier JSON. Le modèle utilisé
pour la classification est un modèle "zero-shot" qui permet de classer les textes sans nécessiter d'entraînement préalable pour les domaines
spécifiques.

Entrées :
- `input_filepath` : Chemin vers un fichier JSON contenant une liste de projets avec leurs abstracts.
- `labels` : Liste des domaines scientifiques utilisés pour la classification.
- `classifier` : Modèle de classification utilisé pour étiqueter les abstracts dans les domaines spécifiés.

Sorties :
- `output_filepath` : Fichier JSON où seront sauvegardées les informations classifiées des projets, ainsi que le nombre de projets par domaine.
"""


def load_json(filepath):
    """Charge les données d'un fichier JSON."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data, filepath):
    """Sauvegarde les données dans un fichier JSON."""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def clean_text(text):
    """Nettoie le texte en remplaçant les caractères spécifiques."""
    if text:
        text = ' '.join(text.split())
    return text

def classify_abstracts(projects, classifier, labels):
    """Classifie les abstracts en utilisant un classificateur de texte."""
    classified_projects = []
    domain_count = Counter()

    for project in tqdm(projects, desc="Classification des abstracts"):
        abstract_content = project.get('abstract', '')
        abstract_content = clean_text(abstract_content)
        if not abstract_content or len(abstract_content.strip()) < 50:  # Trop court ou vide
            continue  # Exclure les abstracts inexploitable

        results = classifier(abstract_content, candidate_labels=labels, multi_label=False)
        best_label = results['labels'][0]
        domain_count[best_label] += 1

        owner = project.get('authors', [{'name': 'Unknown'}])[0]['name']

        classified_projects.append({
            "project_name": project.get('title', 'Unknown Project'),
            "owner": owner,
            "project_url": project.get('softCodeRepository', 'No URL'),
            "description": abstract_content,
            "domain_classification": best_label
        })

    return classified_projects, domain_count

def main(input_filepath, output_filepath):
    # Charger les projets à analyser
    data = load_json(input_filepath)
    projects = data.get('projects', [])

    # Limiter le traitement aux 1000 premiers projets
    projects_to_classify = projects

    # Définir les domaines à classer
    labels = [
        "Biology",
        "Chemistry",
        "Ecology & Environment",
        "Engineering",
        "Mathematics",
        "Nuclear & Particle Physics",
        "Physics",
        "Social Sciences & Humanities",
        "Computer Science",
        "Earth & Universe"
    ]

    # Utiliser un modèle de classification adapté
    classifier = pipeline("zero-shot-classification", model="roberta-large-mnli", device=0 if torch.cuda.is_available() else -1)

    # Classifier les abstracts
    classified_projects, domain_count = classify_abstracts(projects_to_classify, classifier, labels)

    # Ajouter le comptage des domaines à la fin du fichier JSON
    output_data = {
        "projects": classified_projects,
        "domain_counts": domain_count
    }

    # Sauvegarder les résultats
    save_json(output_data, output_filepath)
    print(f"Les classifications des abstracts ont été sauvegardées dans '{output_filepath}'.")

if __name__ == "__main__":
    input_filepath = '../DB/CNRS_REPOS.json'  # Chemin vers le fichier JSON contenant les projets
    output_filepath = 'abstract_classified_all.json'  # Chemin vers le fichier JSON de sortie
    main(input_filepath, output_filepath)
