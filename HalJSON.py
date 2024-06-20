import requests
import re
import json
from itertools import zip_longest

def search_hal_projects(collection, doc_type, start=0, rows=1000):
    """
    Recherche les projets HAL en fonction de la collection et du type de document.
    Permet un paginage pour obtenir tous les résultats.

    Args:
        collection (str): Collection à rechercher.
        doc_type (str): Type de document à rechercher.
        start (int): Indice de départ pour la pagination.
        rows (int): Nombre de résultats par page.

    Returns:
        list: Liste des projets trouvés dans la réponse de l'API.
    """
    fields = "title_s,authFullName_s,authIdHal_s,authIdHal_i,producedDate_s,submittedDate_s,docType_s,labStructName_s,fr_domainAllCodeLabel_fs,abstract_s,keyword_s,halId_s,structName_s,language_s,swhidId_s,softCodeRepository_s,softProgrammingLanguage_s"
    search_url = f"https://api.archives-ouvertes.fr/search/?q=collCode_s:{collection}+AND+docType_s:{doc_type}&start={start}&rows={rows}&fl={fields}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        return response.json().get('response', {}).get('docs', [])
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return []

def collect_hal_data(collection, doc_type):
    """
    Collecte les données des projets HAL pour une collection et un type de document donnés.

    Args:
        collection (str): Collection à rechercher.
        doc_type (str): Type de document à rechercher.

    Returns:
        dict: Dictionnaire catégorisé des projets avec ou sans SWHID et repos.
    """
    all_projects = []
    start, rows = 0, 1000
    while True:
        projects = search_hal_projects(collection, doc_type, start=start, rows=rows)
        if not projects:
            break
        all_projects.extend(projects)
        start += rows
        if len(projects) < rows:
            break

    categorized_projects = {"with_swhid": [], "with_repo": [], "without_swhid_and_repo": []}
    for project in all_projects:
        cleaned_domains = clean_domain_labels(project.get('fr_domainAllCodeLabel_fs', []))
        swhid = project.get('swhidId_s', [''])[0]
        repo = project.get('softCodeRepository_s', [''])[0]
        #On analyse le swhid s'il est present et on extrait le repo, le repo est entre le "origin" et le ";" dans le swhid
        repo_sh= re.search(r'origin=(.*?);', swhid)
        authors = project.get('authFullName_s', [])
        author_auth = project.get('authIdHal_s', [])
        author_id = project.get('authIdHal_i', [])
        
        authors_with_ids = [
            {
                'name': name if name else "",
                'authIdHal_s': id_hal if id_hal else "",
                'authIdHal_i': id_num if id_num else ""
            }
            for name, id_hal, id_num in zip_longest(authors, author_auth, author_id, fillvalue="")
        ]

        project_info = {
            'title': project.get('title_s', [''])[0],
            'authors': authors_with_ids,
            'date': project.get('producedDate_s', ''),
            'submitted_date': project.get('submittedDate_s', ''),
            'type': project.get('docType_s', ''),
            'laboratory': project.get('labStructName_s', [''])[0],
            'domain': ", ".join(cleaned_domains),
            'abstract': project.get('abstract_s', [''])[0],
            'keywords': ", ".join(project.get('keyword_s', [])),
            'hal_id': project.get('halId_s', ''),
            'structures': ", ".join(project.get('structName_s', [])),
            'language': project.get('language_s', '')[0],
            'swhId': swhid,
            'softCodeRepository': repo,
            'softCodeRepository_sh': repo_sh.group(1) if repo_sh else '',
            'forge': repo.split('//')[-1].split('/')[0] if repo else '',
            'softProgrammingLanguage': project.get('softProgrammingLanguage_s', ''),
            'source': 'HAL' 
        }
        if swhid:
            categorized_projects["with_swhid"].append(project_info)
        elif repo:
            categorized_projects["with_repo"].append(project_info)
        else:
            categorized_projects["without_swhid_and_repo"].append(project_info)

    return categorized_projects

def clean_domain_labels(labels):
    """
    Nettoie les étiquettes de domaine pour extraire des noms lisibles.

    Args:
        labels (list): Liste des étiquettes de domaine brutes.

    Returns:
        list: Liste des étiquettes de domaine nettoyées.
    """
    return [re.search(r'_FacetSep_(.*)', label).group(1).split('/')[-1].strip() for label in labels if re.search(r'_FacetSep_(.*)', label)]

def save_json(data, filename):
    """
    Sauvegarde les données dans un fichier JSON.

    Args:
        data (list): Liste des projets à sauvegarder.
        filename (str): Nom du fichier de sortie.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({"number_of_projects": len(data), "projects": [{"project_number": i + 1, **proj} for i, proj in enumerate(data)]}, f, ensure_ascii=False, indent=4)

def merge_json_files(json_files, output_file):
    """
    Fusionne plusieurs fichiers JSON en un seul fichier.

    Args:
        json_files (list): Liste des fichiers JSON à fusionner.
        output_file (str): Nom du fichier de sortie.
    """
    merged_data = []
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_data.extend(data["projects"])

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"number_of_projects": len(merged_data), "projects": merged_data}, f, ensure_ascii=False, indent=4)

def main():
    """
    Collecte les données des projets HAL et les sauvegarde dans des fichiers JSON.
    """
    collection, doc_type = 'CNRS', 'SOFTWARE'
    projects = collect_hal_data(collection, doc_type)
    save_json(projects["with_swhid"], 'CNRS_SWHID.json')
    save_json(projects["with_repo"], 'CNRS_REPO.json')
    save_json(projects["without_swhid_and_repo"], 'CNRS_AUTRE.json')

    #utilisation de la fonction merge_json_files pour fusionner les fichiers JSON en un seul fichier
    json_files = ['CNRS_SWHID.json', 'CNRS_REPO.json']
    merge_json_files(json_files, 'CNRS_HAL.json')

if __name__ == "__main__":
    main()
