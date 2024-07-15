import requests
import json

def read_labs_from_file(file_path):
    labs = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if ':' in line:
                lab_name, url = line.split(':', 1)
                labs[lab_name.strip()] = url.strip()
    return labs

def get_all_public_projects(base_url):
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

def main(input_file, output_file):
    labs = read_labs_from_file(input_file)
    all_labs_data = []

    for lab_name, lab_url in labs.items():
        print(f"Collecte des données pour {lab_name} à partir de {lab_url}...")
        projects = get_all_public_projects(lab_url)
        lab_data = {
            "laboratory_name": lab_name,
            "number_of_projects": len(projects),
            "projects": projects
        }
        all_labs_data.append(lab_data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_labs_data, f, ensure_ascii=False, indent=4)

    print(f"Toutes les informations des laboratoires ont été sauvegardées dans '{output_file}'.")

if __name__ == "__main__":
    input_file = 'labs_gitlab.txt'  # Remplacer par le chemin de votre fichier texte
    output_file = 'labs_projects.json'  # Nom du fichier de sortie
    main(input_file, output_file)
