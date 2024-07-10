import json
import os

""" Prends un fichier texte nommé Nom_du_Laboratoire.txt et contenant une liste d'url et génère un fichier JSON contenant les informations des projets """

def read_links_from_file(file_path):
    """
    Lit les liens à partir d'un fichier texte.
    Args:
        file_path (str): Chemin du fichier texte contenant les liens.
    Returns:
        list: Liste des liens extraits du fichier.
    """
    with open(file_path, 'r') as file:
        links = file.readlines()
    return [link.strip() for link in links]

def extract_project_info(link, lab_name):
    """
    Extrait les informations d'un projet à partir d'un lien et du nom du laboratoire.
    Args:
        link (str): Lien du dépôt de code.
        lab_name (str): Nom du laboratoire.
    Returns:
        dict: Informations extraites du projet.
    """
    parts = link.split('/')
    title = parts[-1]  # Le titre est le dernier élément du lien
    author = parts[3]  # L'auteur est le quatrième élément du lien
    forge = parts[2]  # La forge est le troisième élément du lien
    
    return {
        "title": title,
        "authors": [
            {
                "name": author
            }
        ],
        "softCodeRepository": link,
        "laboratory": lab_name,
        "source": "external",
        "forge": forge
    }

def generate_json_output(links, lab_name):
    """
    Génère une sortie JSON à partir des liens et du nom du laboratoire.
    Args:
        links (list): Liste des liens des projets.
        lab_name (str): Nom du laboratoire.
    Returns:
        dict: Dictionnaire formaté pour la sortie JSON.
    """
    projects = [extract_project_info(link, lab_name) for link in links]
    output = {
        "number_of_projects": len(projects),
        "projects": projects
    }
    return output

def write_json_to_file(data, file_path):
    """
    Écrit les données dans un fichier JSON.
    Args:
        data (dict): Données à écrire dans le fichier JSON.
        file_path (str): Chemin du fichier de sortie JSON.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main(input_file, output_file):
    """
    Fonction principale pour lire les liens à partir d'un fichier texte, générer une sortie JSON et l'écrire dans un fichier.
    Args:
        input_file (str): Chemin du fichier texte d'entrée.
        output_file (str): Chemin du fichier JSON de sortie.
    """
    lab_name = os.path.basename(input_file).replace('.txt', '')  # Déduit le nom du laboratoire à partir du nom du fichier
    links = read_links_from_file(input_file)  # Lit les liens à partir du fichier texte
    json_output = generate_json_output(links, lab_name)  # Génère la sortie JSON
    write_json_to_file(json_output, output_file)  # Écrit la sortie JSON dans un fichier
    print(f"JSON output written to {output_file}")

if __name__ == "__main__":
    input_file = 'Cailloux.txt' 
    output_file = 'ExtJSON.json'
    main(input_file, output_file)
