import requests
import json
import time
import os
import re

'''
    Description : Ce script collecte les informations détaillées des dépôts GitHub pour une liste de propriétaires de dépôts.
    Le script utilise l'API GraphQL de GitHub pour interroger les dépôts d'un propriétaire spécifié, collecte diverses informations 
    comme les langues de programmation utilisées, les sujets du dépôt, le nombre d'étoiles, de forks, et d'autres métadonnées. 
    Il maintient un fichier d'état pour suivre la progression et éviter de retraiter les mêmes dépôts. Les données collectées sont 
    sauvegardées dans un fichier JSON, permettant une analyse ultérieure.

    Entrées :
    - `input_filepath` : Chemin vers un fichier JSON contenant une liste de projets GitHub obtenu du script GithubPreJSON.py
    Sorties :
    - `output_filepath` : Chemin vers le fichier JSON où les informations détaillées des dépôts GitHub seront sauvegardées.
'''

class GitHubRepoInfoFetcher:
    def __init__(self, github_api_token, state_file='owner_SH_state.json'):
        """
        Initialise la classe avec un jeton GitHub et un fichier d'état.
        Args:
            github_api_token (str): Jeton d'authentification GitHub.
            state_file (str): Nom du fichier d'état pour sauvegarder la progression.
        """
        self.github_api_token = github_api_token
        self.headers = {
            'Authorization': f'token {self.github_api_token}',
            'Content-Type': 'application/json'
        }
        self.state_file = state_file
        self.state = self.load_state()

    def load_state(self):
        """
        Charge l'état à partir du fichier d'état ou initialise un nouvel état si le fichier n'existe pas.
        """
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r', encoding='utf-8') as file:
                state = json.load(file)
                state["processed_urls"] = set(state["processed_urls"])  # Convertir en set
        else:
            state = {
                "repos_processed": [],
                "projects": [],
                "project_counter": 1,
                "processed_urls": set()
            }
        return state

    def save_state(self):
        """
        Sauvegarde l'état actuel dans le fichier d'état.
        """
        with open(self.state_file, 'w', encoding='utf-8') as file:
            state_copy = self.state.copy()
            state_copy["processed_urls"] = list(state_copy["processed_urls"])  # Convertir en liste pour sauvegarde
            json.dump(state_copy, file, ensure_ascii=False, indent=4)

    def fetch_repo_info(self, owners):
        """
        Récupère les informations détaillées pour une liste de propriétaires de dépôts.
        Args:
            owners (list): Liste des propriétaires de dépôts GitHub.
        Returns:
            list: Liste des projets avec les informations détaillées.
        """
        for owner in owners:
            print(f"Processing owner: {owner}")
            if owner in self.state['repos_processed']:
                print(f"Owner {owner} already processed, skipping.")
                continue

            try:
                owner_info, repo_data_list = self.fetch_repos_by_owner(owner)
                if not repo_data_list:
                    print(f"No repository data found for owner {owner}")
                    continue

                for repo_data in repo_data_list:
                    if not repo_data:
                        print(f"Empty repository data found for {owner}")
                        continue

                    repo_url = repo_data.get("url", "N/A")
                    if repo_url in self.state["processed_urls"]:
                        print(f"Duplicate URL found: {repo_url}")
                        continue

                    languages = [lang['name'] for lang in repo_data.get('languages', {}).get('nodes', [])]

                    project_data = {
                        "project_number": self.state['project_counter'],
                        "title": repo_data.get('name', 'N/A'),
                        "authors": [owner_info],
                        "submitted_date": repo_data.get("createdAt", "N/A"),
                        "updated_date": repo_data.get("updatedAt", "N/A"),
                        "laboratory": owner_info["Github_full_name"] if owner_info["kind"] == "organization" else "",
                        "abstract": repo_data.get("description", "N/A"),
                        "keywords": ", ".join([topic['topic']['name'] for topic in repo_data.get("repositoryTopics", {}).get("nodes", [])]),
                        "github_id": repo_data.get("id", "N/A"),
                        "softCodeRepository": repo_url,
                        "forge": "github.com",
                        "softProgrammingLanguage": languages,
                        "source": "Github_modality_1",
                        "repo_info": self.collect_info(repo_data)
                    }
                    self.state['projects'].append(project_data)
                    self.state['project_counter'] += 1
                    self.state["processed_urls"].add(repo_url)

            except requests.exceptions.RequestException as e:
                print(f"RequestException for owner {owner}: {e}")
                self.state['projects'].append({
                    "project_number": self.state['project_counter'],
                    "title": "none",
                    "authors": [
                        {
                            "name": owner,
                            "AuthGithubId": "none"
                        }
                    ],
                    "submitted_date": "none",
                    "updated_date": "none",
                    "laboratory": "none",
                    "abstract": "none",
                    "keywords": "none",
                    "github_id": "none",
                    "softCodeRepository": "none",
                    "forge": "github.com",
                    "softProgrammingLanguage": [],
                    "source": "GitHub"
                })
                self.state['project_counter'] += 1
            
            self.state['repos_processed'].append(owner)
            self.save_state()
            time.sleep(1)  # Sleep to avoid hitting rate limits too quickly

        return self.state['projects']


    def fetch_repos_by_owner(self, owner):
        """
        Récupère les données de tous les dépôts d'un propriétaire GitHub.
        Args:
            owner (str): Nom du propriétaire du dépôt GitHub.
        Returns:
            tuple: (owner_info, list): Informations du propriétaire et liste des données des dépôts GitHub.
        """
        query = """
        query ($owner: String!, $after: String) {
        user(login: $owner) {
            id
            login
            name
            company
            websiteUrl
            location
            email
            repositories(first: 100, after: $after) {
            totalCount
            pageInfo {
                hasNextPage
                endCursor
            }
            nodes {
                id
                name
                description
                createdAt
                updatedAt
                pushedAt
                diskUsage
                isArchived
                hasWikiEnabled
                stargazerCount
                forkCount
                owner {
                login
                id
                }
                watchers {
                totalCount
                }
                issues {
                totalCount
                }
                url
                homepageUrl
                languages(first: 10) {
                nodes {
                    name
                }
                }
                commitCount: object(expression: "HEAD") {
                ... on Commit {
                    history {
                    totalCount
                    }
                }
                }
                repositoryTopics(first: 10) {
                nodes {
                    topic {
                    name
                    }
                }
                }
            }
            }
        }
        organization(login: $owner) {
            id
            login
            name
            websiteUrl
            location
            email
            repositories(first: 100, after: $after) {
            totalCount
            pageInfo {
                hasNextPage
                endCursor
            }
            nodes {
                id
                name
                description
                createdAt
                updatedAt
                pushedAt
                diskUsage
                isArchived
                hasWikiEnabled
                stargazerCount
                forkCount
                owner {
                login
                id
                }
                watchers {
                totalCount
                }
                issues {
                totalCount
                }
                url
                homepageUrl
                languages(first: 10) {
                nodes {
                    name
                }
                }
                commitCount: object(expression: "HEAD") {
                ... on Commit {
                    history {
                    totalCount
                    }
                }
                }
                repositoryTopics(first: 10) {
                nodes {
                    topic {
                    name
                    }
                }
                }
            }
            }
        }
        }
        """

        variables = {"owner": owner}
        all_repos = []
        owner_info = None

        while True:
            response = requests.post(
                'https://api.github.com/graphql',
                headers=self.headers,
                json={'query': query, 'variables': variables}
            )

            if response.status_code == 200:
                json_data = response.json()
                user_data = json_data.get('data', {}).get('user', {})
                org_data = json_data.get('data', {}).get('organization', {})

                if user_data and 'repositories' in user_data:
                    repos = user_data['repositories']['nodes']
                    all_repos.extend(repos)
                    page_info = user_data['repositories']['pageInfo']
                    owner_info = {
                        "kind": "user",
                        "name": user_data.get("login"),
                        "Github_full_name": user_data.get("name"),
                        "Github_id": user_data.get("id"),
                        "company": user_data.get("company"),
                        "blog": user_data.get("websiteUrl"),
                        "location": user_data.get("location"),
                        "email": user_data.get("email"),
                        "public_repos": user_data['repositories']['totalCount']
                    }
                elif org_data and 'repositories' in org_data:
                    repos = org_data['repositories']['nodes']
                    all_repos.extend(repos)
                    page_info = org_data['repositories']['pageInfo']
                    owner_info = {
                        "kind": "organization",
                        "name": org_data.get("login"),
                        "Github_full_name": org_data.get("name"),
                        "Github_id": org_data.get("id"),
                        "blog": org_data.get("websiteUrl"),
                        "location": org_data.get("location"),
                        "email": org_data.get("email"),
                        "public_repos": org_data['repositories']['totalCount']
                    }
                else:
                    print(f"Invalid response data structure for owner {owner}: {json_data}")
                    break

                if page_info['hasNextPage']:
                    print(f"Fetching next page for {owner}")
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
                print(f"Failed to fetch repos for {owner}: {response.status_code}, {response.text}")
                break

        return owner_info, all_repos

    def collect_info(self, repo_data):
        """
        Collecte les informations pertinentes d'un dépôt GitHub.
        Args:
            repo_data (dict): Données du dépôt GitHub.
        Returns:
            dict: Informations collectées.
        """
        return {
            "name": repo_data.get("name"),
            "full_name": f"{repo_data['owner']['login']}/{repo_data.get('name')}",
            "description": repo_data.get("description"),
            "stars": repo_data.get("stargazerCount"),
            "forks": repo_data.get("forkCount"),
            "owner": repo_data["owner"].get("login"),
            "subscribers": repo_data["watchers"].get("totalCount"),
            "open_issues": repo_data["issues"].get("totalCount"),
            "created_at": repo_data.get("createdAt"),
            "updated_at": repo_data.get("updatedAt"),
            "pushed_at": repo_data.get("pushedAt"),
            "size": repo_data.get("diskUsage"),
            "archived": repo_data.get("isArchived"),
            "has_wiki": repo_data.get("hasWikiEnabled"),
            "homepage": repo_data.get("homepageUrl"),
            "repo_url": repo_data.get("url"),
            "commit_count": repo_data["commitCount"]["history"].get("totalCount") if repo_data.get("commitCount") else 0
        }


    def extract_repo_name(self, url):
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
            owner, _ = GitHubRepoInfoFetcher.extract_repo_name(GitHubRepoInfoFetcher, github_url)
            if owner:
                owners.add(owner)
    return owners

if __name__ == "__main__":
    input_filepath = 'CNRS_GITHUB_FROM_SH.json'  # Chemin vers le fichier JSON d'entrée
    output_filepath = 'CNRS_GITHUB_SH_COMPLET.json'  # Chemin vers le fichier JSON de sortie
    github_api_token = 'use_your_token_here'

    input_data = load_input_json(input_filepath)
    owners = extract_owners_from_projects(input_data['projects'])

    print(f"Extracted owners: {owners}")

    if not owners:
        print("No owners found. Exiting...")
    else:
        fetcher = GitHubRepoInfoFetcher(github_api_token)
        projects = fetcher.fetch_repo_info(owners)

        # Inclure "number_of_projects" au début du JSON de sortie
        output_data = {
            "number_of_projects": len(fetcher.state['projects']),
            "projects": fetcher.state['projects']
        }

        save_output_json(output_data, output_filepath)
        print(f"Les informations sur les projets ont été sauvegardées dans '{output_filepath}'.")

        # Suppression du fichier d'état après avoir terminé
        if os.path.exists(fetcher.state_file):
            os.remove(fetcher.state_file)
            print(f"Le fichier d'état '{fetcher.state_file}' a été supprimé.")
