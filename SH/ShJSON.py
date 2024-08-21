import requests
import logging
import json
import os
import time

# Description : Ce script récupère les informations détaillées des projets archivés sur Software Heritage
# en utilisant l'API Software Heritage. Le script prend en entrée un fichier JSON contenant une liste
# d'URLs de projets (input_file), fichier renvoyé par le script "ShAllProjJSON.py". Pour chaque URL, il extrait 
# des informations sur les visites, les snapshots, et les révisions associées. Ces informations sont ensuite structurées
# et sauvegardées dans un fichier JSON de sortie (output_file). Ce fichier de sortie contient les détails des projets, 
# tels que le titre, les auteurs, l'identifiant du projet sur Software Heritage, la date de soumission, la date de mise à jour, etc. 

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_last_visit_info(origin_url, headers):
    """
    Récupère les informations de la dernière visite d'un dépôt.

    Args:
        origin_url (str): URL du dépôt.
        headers (dict): En-têtes HTTP avec le token d'autorisation.

    Returns:
        dict: Réponse JSON contenant les informations de la dernière visite ou None en cas d'erreur.
    """
    url_latest_visit = f"https://archive.softwareheritage.org/api/1/origin/{origin_url}/visit/latest/"
    while True:
        response = requests.get(url_latest_visit, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            logging.error(f"Erreur 429 : Limite de taux dépassée. Attente de 60 secondes avant de réessayer...")
            time.sleep(60)
        else:
            logging.error(f"Erreur {response.status_code} lors de la récupération de la dernière visite.")
            return None

def get_snapshot_info(snapshot_id, headers):
    """
    Récupère les informations du snapshot.

    Args:
        snapshot_id (str): ID du snapshot.
        headers (dict): En-têtes HTTP avec le token d'autorisation.

    Returns:
        dict: Réponse JSON contenant les informations du snapshot ou None en cas d'erreur.
    """
    url_snapshot = f"https://archive.softwareheritage.org/api/1/snapshot/{snapshot_id}/"
    while True:
        response = requests.get(url_snapshot, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            logging.error(f"Erreur 429 : Limite de taux dépassée. Attente de 60 secondes avant de réessayer...")
            time.sleep(60)
        else:
            logging.error(f"Erreur {response.status_code} lors de la récupération du snapshot.")
            return None

def get_revision_info(revision_id, headers):
    """
    Récupère les informations de la révision.

    Args:
        revision_id (str): ID de la révision.
        headers (dict): En-têtes HTTP avec le token d'autorisation.

    Returns:
        dict: Réponse JSON contenant les informations de la révision ou None en cas d'erreur.
    """
    url_revision = f"https://archive.softwareheritage.org/api/1/revision/{revision_id}/"
    while True:
        response = requests.get(url_revision, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            logging.error(f"Erreur 429 : Limite de taux dépassée. Attente de 60 secondes avant de réessayer...")
            time.sleep(60)
        else:
            logging.error(f"Erreur {response.status_code} lors de la récupération de la révision.")
            return None

def get_project_info(origin_url, headers):
    """
    Récupère les informations détaillées sur un projet.

    Args:
        origin_url (str): URL du dépôt du projet.
        headers (dict): En-têtes HTTP avec le token d'autorisation.

    Returns:
        dict: Dictionnaire contenant les informations détaillées du projet.
    """
    visit_info = get_last_visit_info(origin_url, headers)
    if not visit_info:
        return {}

    snapshot_id = visit_info.get('snapshot')
    snapshot_info = get_snapshot_info(snapshot_id, headers)
    if not snapshot_info:
        return {}

    branches = snapshot_info.get('branches', {})
    revision_id = None
    if "refs/heads/main" in branches:
        revision_id = branches['refs/heads/main']['target']
    else:
        for key in branches:
            if key != 'HEAD':
                revision_id = branches[key]['target']
                break

    revision_info = get_revision_info(revision_id, headers) if revision_id else {}
    
    title = os.path.basename(origin_url).replace('.git', '').replace('_', ' ').replace('-', ' ')

    authors = []
    if revision_info:
        author_name = revision_info.get('author', {}).get('name', 'Unknown')
        author_email = revision_info.get('author', {}).get('email', 'Unknown')
        authors.append({"name": author_name, "mail": author_email})

    project_info = {
        "title": title,
        "authors": authors,
        "sh_id": revision_id,
        "abstract": revision_info.get('message', 'Unknown') if revision_info else 'Unknown',
        "submitted_date": revision_info.get('date', 'Unknown') if revision_info else 'Unknown',
        "updated_date": visit_info.get('date', 'Unknown'),
        "softCodeRepository": origin_url,
        "domain": "",  
        "language": "",
        "laboratory": "",
        "keyword": "",
        "source": "Software_heritage",
    }
    
    return project_info

def main(input_file, output_file, token):
    """
    Fonction principale pour récupérer les données de projets et les sauvegarder dans un fichier JSON.

    Args:
        input_file (str): Chemin vers le fichier JSON d'entrée contenant les URLs des projets.
        output_file (str): Chemin vers le fichier JSON de sortie pour sauvegarder les informations des projets.
        token (str): Token d'autorisation pour l'API Software Heritage.
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    # Charger le fichier d'entrée
    try:
        with open(input_file, "r", encoding='utf-8') as file:
            input_data = json.load(file)
            projects = input_data.get("projects", [])
            logging.info(f"{len(projects)} projets chargés depuis le fichier d'entrée.")
    except FileNotFoundError:
        logging.error(f"Fichier d'entrée {input_file} introuvable.")
        return
    
    # Charger le fichier de sortie existant s'il existe
    if os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding='utf-8') as file:
                structured_data = json.load(file)
                existing_urls = {project["softCodeRepository"] for project in structured_data["projects"]}
        except json.JSONDecodeError:
            logging.error("Erreur lors du décodage du fichier de sortie, démarrage avec un nouveau fichier.")
            structured_data = {"number_of_projects": 0, "projects": []}
            existing_urls = set()
    else:
        structured_data = {"number_of_projects": 0, "projects": []}
        existing_urls = set()

    # Traiter chaque projet dans le fichier d'entrée
    for project in projects:
        origin_url = project.get("url", "N/A")
        if origin_url in existing_urls or origin_url == "N/A":
            continue
        
        project_info = get_project_info(origin_url, headers)
        if project_info:
            structured_data["projects"].append(project_info)
            structured_data["number_of_projects"] += 1

            # Sauvegarder le fichier de sortie après chaque projet
            with open(output_file, "w", encoding='utf-8') as file:
                json.dump(structured_data, file, ensure_ascii=False, indent=4)
            logging.info(f"Projet {project_info['title']} ajouté au fichier de sortie.")

    logging.info(f"Données structurées sauvegardées dans {output_file}")

if __name__ == "__main__":
    input_file = "SH_CNRS_PROJ.json" 
    output_file = "SH_CNRS.json"  
    token = "your_token_here"
    main(input_file, output_file, token)
