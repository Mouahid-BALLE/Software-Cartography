import requests
import json

# Lire le fichier JSON d'entrée
with open('all_labs_projects.json', 'r', encoding='utf-8') as f:
    input_json = json.load(f)

# Fonction pour transformer les projets
def transform_projects(input_json):
    transformed_projects = []
    total_projects = 0

    for lab_data in input_json:
        for project in lab_data["projects"]:
            transformed_project = {
                "title": project.get('name', ''),
                "authors": [
                    {
                        "name": project['namespace'].get('name', ''),
                        "AuthGitlabId": project['namespace'].get('id', ''),
                        "kind": project['namespace'].get('kind', '')
                    }
                ],
                "submitted_date": project.get('created_at', '').split('T')[0],
                "updated_date": project.get('last_activity_at', ''),
                "type": "SOFTWARE",
                "laboratory": lab_data["laboratory_name"],
                "domain": ", ".join(project.get('topics', [])),
                "abstract": project.get('description', ''),
                "keywords": ", ".join(project.get('tag_list', [])),
                "softCodeRepository": project.get('web_url', ''),
                "readme": project.get('readme_url', ''),
                "stars": project.get('star_count', 0),
                "forks": project.get('forks_count', 0),
                "gitlab_id": project['id'],
                "forge": "gitlab",
                "source": "gitLab",
            }
            transformed_projects.append(transformed_project)
        total_projects += lab_data["number_of_projects"]

    output_json = {
        "number_of_projects": total_projects,
        "projects": transformed_projects
    }
    return output_json

# Transformer les projets
output_json = transform_projects(input_json)

# Sauvegarder les projets transformés dans un fichier JSON
with open('transformed_projects.json', 'w', encoding='utf-8') as f:
    json.dump(output_json, f, ensure_ascii=False, indent=4)

print("Les informations des projets transformés ont été sauvegardées dans 'transformed_projects.json'.")
