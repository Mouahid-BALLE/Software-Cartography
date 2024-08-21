import json

# Description : Ce script lit un fichier JSON contenant des projets issus de diverses instances GitLab,
# transforme ces données pour les structurer dans un format spécifique, et les sauvegarde dans un nouveau
# fichier JSON. Chaque projet est enrichi avec des informations comme le nom du projet, les auteurs, les dates
# de création et de dernière mise à jour, les mots-clés, le nombre d'étoiles, le nombre de forks, et d'autres
# détails pertinents.

# Entrées :
# - Fichier JSON 'concatenated_projects.json' contenant les données brutes des projets.

# Sorties :
# - Fichier JSON 'transformed_projects.json' contenant les projets transformés avec les nouvelles structures de données.

# Lire le fichier JSON d'entrée
with open('concatenated_projects.json', 'r', encoding='utf-8') as f:
    input_json = json.load(f)

def transform_projects(input_json):
    """
    Transforme les projets issus du fichier JSON d'entrée en une structure plus riche et détaillée.

    Args:
        input_json (list): Liste des projets provenant de différentes instances GitLab.

    Returns:
        dict: Dictionnaire contenant le nombre total de projets et une liste de projets transformés.
    """
    transformed_projects = []
    total_projects = 0

    for lab_data in input_json:
        # Parcourt chaque projet pour appliquer la transformation
        for project in lab_data["projects"]:
            transformed_project = {
                "title": project.get('name', ''),  # Nom du projet
                "authors": [
                    {
                        "name": project['namespace'].get('name', '') if 'namespace' in project else '',
                        "AuthGitlabId": project['namespace'].get('id', '') if 'namespace' in project else '',
                        "kind": project['namespace'].get('kind', '') if 'namespace' in project else ''
                    }
                ],
                "submitted_date": project.get('created_at', '').split('T')[0],  # Date de soumission
                "updated_date": project.get('last_activity_at', ''),  # Date de dernière mise à jour
                "type": "SOFTWARE",  # Type de document
                "laboratory": lab_data.get("laboratory_name", ""),  # Nom du laboratoire
                "domain": ", ".join(project.get('topics', [])),  # Domaine(s) du projet
                "abstract": project.get('description', ''),  # Description du projet
                "keywords": ", ".join(project.get('tag_list', [])),  # Mots-clés associés
                "softCodeRepository": project.get('web_url', ''),  # URL du dépôt GitLab
                "readme": project.get('readme_url', ''),  # URL du fichier README
                "stars": project.get('star_count', 0),  # Nombre d'étoiles du projet
                "forks": project.get('forks_count', 0),  # Nombre de forks du projet
                "gitlab_id": project['id'],  # Identifiant unique du projet sur GitLab
                "forge": lab_data.get('forge_name', ''),  # Nom de la forge
                "source": "gitLab",  # Source des données
            }
            transformed_projects.append(transformed_project)
        total_projects += lab_data["number_of_projects"]

    output_json = {
        "number_of_projects": total_projects,  # Nombre total de projets transformés
        "projects": transformed_projects  # Liste des projets transformés
    }
    return output_json

# Transformer les projets
output_json = transform_projects(input_json)

# Sauvegarder les projets transformés dans un fichier JSON
with open('transformed_projects.json', 'w', encoding='utf-8') as f:
    json.dump(output_json, f, ensure_ascii=False, indent=4)

print("Les informations des projets transformés ont été sauvegardées dans 'transformed_projects.json'.")
