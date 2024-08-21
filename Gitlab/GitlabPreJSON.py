import requests
import json
from urllib.parse import urlparse

# Description : Ce script récupère les informations sur les projets publics hébergés sur différentes instances GitLab,
# à partir d'une liste de laboratoires (et leurs URLs) fournie dans un fichier texte. Le script parcourt chaque laboratoire
# et récupère tous les projets publics disponibles sur la forge GitLab correspondante. Les informations collectées pour chaque
# laboratoire sont ensuite sauvegardées dans un fichier JSON de sortie. Ce fichier de sortie contient des détails sur chaque forge,
# comme le nom du laboratoire, le nom de la forge, et la liste des projets publics associés.

# Entrées :
# - `input_file` : Chemin vers un fichier texte contenant les noms des laboratoires et leurs URLs GitLab correspondantes.
#
# Sorties :
# - `output_file` : Fichier JSON contenant les informations sur les projets publics pour chaque laboratoire spécifié.

def read_labs_from_file(file_path):
    """
    Lit un fichier texte pour extraire les noms des laboratoires et leurs URLs GitLab correspondantes.

    Args:
        file_path (str): Chemin vers le fichier texte contenant les laboratoires et leurs URLs.

    Returns:
        dict: Dictionnaire avec les noms des laboratoires comme clés et leurs URLs comme valeurs.
    """
    labs = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if ':' in line:
                lab_name, url = line.split(':', 1)
                labs[lab_name.strip()] = url.strip()
    return labs

def get_all_public_projects(base_url):
    """
    Récupère tous les projets publics d'une instance GitLab donnée en utilisant l'API GitLab.

    Args:
        base_url (str): URL de base de l'instance GitLab.

    Returns:
        list: Liste des projets publics récupérés depuis l'instance GitLab.
    """
    per_page = 100  # Nombre maximum de projets par page autorisé par l'API
    projects = []
    page = 1

    while True:
        url = f"{base_url}/api/v4/projects?visibility=public&per_page={per_page}&page={page}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Vérifie si la requête a échoué
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête à {base_url}: {e}")
            break

        data = response.json()
        if not data:
            break

        projects.extend(data)
        page += 1

    return projects

def extract_forge_name(url):
    """
    Extrait le nom de la forge à partir de l'URL.

    Args:
        url (str): URL complète de la forge.

    Returns:
        str: Nom de la forge (nom de domaine).
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc

def main(input_file, output_file):
    """
    Fonction principale qui lit le fichier des laboratoires, collecte les projets publics pour chaque laboratoire
    et enregistre les résultats dans un fichier JSON.

    Args:
        input_file (str): Chemin vers le fichier texte contenant les laboratoires et leurs URLs.
        output_file (str): Chemin vers le fichier JSON de sortie.
    """
    labs = read_labs_from_file(input_file)
    all_labs_data = []

    for lab_name, lab_url in labs.items():
        forge_name = extract_forge_name(lab_url)
        print(f"Collecte des données pour la forge {forge_name} à partir de {lab_url}...")
        projects = get_all_public_projects(lab_url)
        
        # Structure différente pour LAB_RESERVED_GITLAB.txt
        if input_file == 'LAB_RESERVED_GITLAB.txt':
            lab_data = {
                "laboratory_name": lab_name,
                "forge_name": forge_name,
                "number_of_projects": len(projects),
                "projects": projects
            }
        else:
            lab_data = {
                "forge_name": forge_name,
                "number_of_projects": len(projects),
                "projects": projects
            }
        
        all_labs_data.append(lab_data)

    # Sauvegarde des données collectées dans un fichier JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_labs_data, f, ensure_ascii=False, indent=4)

    print(f"Toutes les informations des forges ont été sauvegardées dans '{output_file}'.")

if __name__ == "__main__":
    input_file = 'LAB_ON_SHARED_GITLAB.txt'  # Remplacer par le chemin de votre fichier texte
    output_file = 'LAB_ON_SHARED_GITLAB.json'  # Nom du fichier de sortie
    main(input_file, output_file)
