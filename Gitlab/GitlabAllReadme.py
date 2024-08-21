import requests
import json
from urllib.parse import quote
import time

# Description : Ce script collecte des informations sur les projets publics hébergés sur différentes instances GitLab,
# extrait les contenus des fichiers README de chaque projet, puis les sauvegarde dans un fichier JSON. Le script lit
# les URLs des laboratoires depuis un fichier texte, interroge les API GitLab pour récupérer les projets publics,
# et tente de télécharger le contenu des fichiers README associés.

# Entrées :
# - `input_file` : Chemin vers un fichier texte contenant les noms des laboratoires et leurs URLs GitLab correspondantes.
#
# Sorties :
# - `output_file` : Fichier JSON contenant les projets avec leurs contenus README récupérés.

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

def get_all_projects(base_url):
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
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête à {base_url}: {e}")
            break

        data = response.json()
        if not data:
            break

        projects.extend(data)
        page += 1

    return projects

def get_readme_content(base_url, project_id, retries=3):
    """
    Récupère le contenu du fichier README d'un projet GitLab donné.

    Args:
        base_url (str): URL de base de l'instance GitLab.
        project_id (int): ID du projet GitLab.
        retries (int): Nombre de tentatives en cas d'échec de la requête.

    Returns:
        str: Contenu du fichier README ou None en cas d'échec.
    """
    file_path = "README.md"
    url = f"{base_url}/api/v4/projects/{project_id}/repository/files/{quote(file_path)}/raw"
    attempt = 0

    while attempt < retries:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.Timeout:
            attempt += 1
            print(f"Erreur de temporisation lors de la requête pour le projet {project_id}. Réessayer {attempt}/{retries}...")
            time.sleep(1)  # Attendre 1 seconde avant de réessayer
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(f"README non trouvé pour le projet {project_id}.")
            else:
                print(f"Erreur lors de la requête pour le projet {project_id}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête pour le projet {project_id}: {e}")
            return None

    print(f"Échec des tentatives pour récupérer le README du projet {project_id} après {retries} essais.")
    return None

def main(input_file, output_file):
    """
    Fonction principale qui lit le fichier des laboratoires, collecte les projets publics pour chaque laboratoire,
    extrait les contenus des fichiers README des projets et enregistre les résultats dans un fichier JSON.

    Args:
        input_file (str): Chemin vers le fichier texte contenant les laboratoires et leurs URLs.
        output_file (str): Chemin vers le fichier JSON de sortie.
    """
    labs = read_labs_from_file(input_file)
    all_projects = []

    for lab_name, lab_url in labs.items():
        print(f"Collecte des données pour la forge {lab_url}...")
        projects = get_all_projects(lab_url)
        for project in projects:
            if 'default_branch' in project:
                readme_url = f"{lab_url}/{project['path_with_namespace']}/-/blob/{project['default_branch']}/README.md"
                all_projects.append({
                    "title": project['name'],
                    "project_url": project['web_url'],
                    "readme_url": readme_url,
                    "gitlab_id": project['id'],
                    "forge": lab_url
                })
            else:
                print(f"Le projet {project['name']} n'a pas de branche par défaut.")

    readme_contents = []
    for project in all_projects:
        readme_content = get_readme_content(project['forge'], project['gitlab_id'])
        if readme_content:
            readme_contents.append({
                "project_name": project['title'],
                "project_url": project['project_url'],
                "readme_url": project['readme_url'],
                "readme_content": readme_content
            })

    # Sauvegarder les contenus README dans un fichier JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(readme_contents, f, ensure_ascii=False, indent=4)

    print(f"Les contenus des fichiers README ont été sauvegardés dans '{output_file}'.")

if __name__ == "__main__":
    input_file = 'labs_gitlab.txt'  # Remplacer par le chemin de votre fichier texte contenant les URLs des laboratoires
    output_file = 'LABS_GITLAB_README.json'  # Nom du fichier de sortie

    main(input_file, output_file)
