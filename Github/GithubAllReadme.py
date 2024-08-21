import requests
import json
import re
import time

"""
Description : Ce script extrait les informations sur les dépôts GitHub d'un propriétaire spécifié (utilisateur ou organisation)
et récupère le contenu des fichiers README associés à ces dépôts. Le script interroge l'API GraphQL de GitHub pour obtenir la liste
des dépôts, puis tente de récupérer et de stocker le contenu du fichier README de chaque dépôt. Les informations récupérées sont
ensuite sauvegardées dans un fichier JSON pour une analyse ultérieure.

Entrées :
- `input_filepath` : Chemin vers un fichier JSON contenant une liste de projets avec des URLs de dépôts GitHub, fichier généré par GithubJSON.py
Sorties :
- `output_filepath` : Fichier JSON où seront sauvegardées les informations des dépôts GitHub et le contenu des fichiers README.
"""


def fetch_repos_and_readmes(owner, token):
    """
    Récupère la liste des dépôts et le contenu des README d'un utilisateur ou organisation GitHub.
    Args:
        owner (str): Nom du propriétaire du dépôt GitHub.
        token (str): Jeton d'accès GitHub.
    Returns:
        list: Liste des informations sur les dépôts avec le contenu du README décodé.
    """
    url = "https://api.github.com/graphql"
    query = """
    query($owner: String!, $after: String) {
      user(login: $owner) {
        repositories(first: 100, after: $after) {
          nodes {
            name
            url
            object(expression: "HEAD:README.md") {
              ... on Blob {
                text
              }
            }
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
      organization(login: $owner) {
        repositories(first: 100, after: $after) {
          nodes {
            name
            url
            object(expression: "HEAD:README.md") {
              ... on Blob {
                text
              }
            }
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
    """
    headers = {
        'Authorization': f'bearer {token}',
        'Content-Type': 'application/json'
    }
    variables = {'owner': owner, 'after': None}
    all_repos = []

    while True:
        response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

        if response.status_code == 200:
            data = response.json()
            user_data = data['data'].get('user', {})
            org_data = data['data'].get('organization', {})
            
            if user_data and 'repositories' in user_data:
                repos = user_data['repositories']['nodes']
                page_info = user_data['repositories']['pageInfo']
            elif org_data and 'repositories' in org_data:
                repos = org_data['repositories']['nodes']
                page_info = org_data['repositories']['pageInfo']
            else:
                print(f"No repositories found for owner {owner}")
                break
            
            for repo in repos:
                readme_content = repo['object']['text'] if repo['object'] else "README.md not found"
                all_repos.append({
                    "project_name": repo['name'],
                    "owner": owner,
                    "project_url": repo['url'],
                    "readme_url": repo['url'] + "/blob/master/README.md",
                    "readme_content": readme_content
                })

            if page_info['hasNextPage']:
                variables['after'] = page_info['endCursor']
            else:
                break
        elif response.status_code == 403:
            if 'X-RateLimit-Reset' in response.headers:
                reset_time = int(response.headers['X-RateLimit-Reset'])
                current_time = int(time.time())
                sleep_time = reset_time - current_time + 1
                if sleep_time > 0:
                    print(f"Rate limit exceeded, sleeping until reset time: {sleep_time} seconds")
                    time.sleep(sleep_time)
                continue
            else:
                print("Rate limit exceeded, no reset time provided. Sleeping for 1 hour by default.")
                time.sleep(3600)  # Sleep for 1 hour by default
                continue
        else:
            print(f"Failed to fetch repositories for {owner}: {response.status_code}")
            break

    return all_repos

def load_input_json(filepath):
    """
    Charge les données d'un fichier JSON.
    Args:
        filepath (str): Chemin vers le fichier JSON.
    Returns:
        dict: Données JSON chargées.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_output_json(data, filepath):
    """
    Sauvegarde les données dans un fichier JSON.
    Args:
        data (dict): Données à sauvegarder.
        filepath (str): Chemin vers le fichier de sortie.
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def extract_owners_from_projects(projects):
    """
    Extrait les propriétaires des dépôts à partir des projets.
    Args:
        projects (list): Liste des projets.
    Returns:
        set: Ensemble des propriétaires de dépôts.
    """
    owners = set()
    for project in projects:
        github_url = project.get("repo_url")
        if github_url:
            owner, _ = extract_repo_name(github_url)
            if owner:
                owners.add(owner)
    return owners

def extract_repo_name(url):
    """
    Extrait le propriétaire et le nom du dépôt GitHub à partir de l'URL.
    Args:
        url (str): URL du dépôt GitHub.
    Returns:
        tuple: (propriétaire, nom du dépôt)
    """
    if not isinstance(url, str):
        return None, None
    match = re.search(r'github\.com/([^/]+)/([^/]+)', url)
    if match:
        return match.group(1), match.group(2)
    return None, None

if __name__ == "__main__":
    
    input_filepath = 'CNRS_GITHUB_FROM_SH.json'  # Chemin vers le fichier JSON d'entrée
    output_filepath = 'README_SH.json'  # Chemin vers le fichier JSON de sortie
    github_api_token = 'use_your_token_here'

    input_data = load_input_json(input_filepath)
    owners = extract_owners_from_projects(input_data['projects'])

    print(f"Extracted owners: {owners}")

    all_readmes = []
    for owner in owners:
        readmes = fetch_repos_and_readmes(owner, github_api_token)
        all_readmes.extend(readmes)

    save_output_json(all_readmes, output_filepath)
    print(f"Les informations des projets et les contenus des README ont été sauvegardés dans '{output_filepath}'.")
