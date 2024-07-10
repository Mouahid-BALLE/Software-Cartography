import requests
import json
import time
import os

""" A partir du fichier généré par Github/GitJSON.py, on va extraire les propriétaires des dépôts GitHub et récupérer les informations
de base de ces dépôts."""

class GitHubRepoFetcher:
    def __init__(self, github_api_token, state_file='owner_state.json'):
        """
        Initialise la classe avec un jeton GitHub et un fichier d'état.
        Args:
            github_api_token (str): Jeton d'authentification GitHub.
            state_file (str): Nom du fichier d'état pour sauvegarder la progression.
        """
        self.github_api_token = github_api_token
        self.headers = {
            'Authorization': f'token {self.github_api_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.state_file = state_file
        self.load_state()

    def load_state(self):
        """
        Charge l'état à partir du fichier d'état.
        """
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r', encoding='utf-8') as file:
                self.state = json.load(file)
        else:
            self.state = {
                "owners_processed": [],
                "projects": [],
                "project_counter": 1
            }

    def save_state(self):
        """
        Sauvegarde l'état actuel dans le fichier d'état.
        """
        with open(self.state_file, 'w', encoding='utf-8') as file:
            json.dump(self.state, file, ensure_ascii=False, indent=4)

    def fetch_repos(self, owners):
        """
        Récupère les informations des dépôts pour une liste de propriétaires.
        Args:
            owners (list): Liste des propriétaires de dépôts GitHub.
        Returns:
            dict: Dictionnaire contenant le nombre de projets et les informations des projets.
        """
        for owner in owners:
            if owner in self.state['owners_processed']:
                continue

            try:
                repos = self.fetch_user_repos(owner)
                for repo in repos:
                    repo_data = self.fetch_repo(owner, repo['name'])
                    if repo_data:
                        contributors = self.fetch_repo_contributors(owner, repo['name'])
                        organization = repo_data.get("organization", {"login": ""})
                        topics = ", ".join(repo.get("topics", [])) if repo.get("topics") else ""
                        languages = [repo.get("language", "")] if repo.get("language") else []
                        project_data = {
                            "project_number": self.state['project_counter'],
                            "title": repo.get("name", ""),
                            "authors": contributors,
                            "submitted_date": repo.get("created_at", ""),
                            "updated_date": repo.get("updated_at", ""),
                            "laboratory": organization.get("login", ""),
                            "domain": topics,
                            "abstract": repo.get("description", ""),
                            "keywords": "",
                            "github_id": repo.get("id", ""),
                            "structures": "",
                            "softCodeRepository": repo.get("html_url", ""),
                            "forge": "github.com",
                            "softProgrammingLanguage": languages,
                            "source": "Github_modality_1",
                            "hal_id": "",
                            "authIdHal_s": "",    
                            "authIdHal_i": ""
                        }
                        self.state['projects'].append(project_data)
                        self.state['project_counter'] += 1

            except requests.exceptions.RequestException as e:
                self.state['projects'].append({
                    "project_number": self.state['project_counter'],
                    "title": "none",
                    "authors": [{
                        "name": owner,
                        "AuthGithubId": owner
                    }],
                    "submitted_date": "none",
                    "updated_date": "none",
                    "laboratory": "none",
                    "domain": "none",
                    "abstract": "none",
                    "keywords": "none",
                    "hal_id": "none",
                    "structures": "none",
                    "softCodeRepository": "none",
                    "forge": "github.com",
                    "softProgrammingLanguage": "none",
                    "source": "GitHub",
                    "error": f"API request failed: {str(e)}"
                })
                self.state['project_counter'] += 1
            
            self.state['owners_processed'].append(owner)
            self.save_state()
            time.sleep(1)  # Sleep to avoid hitting rate limits too quickly

        return {
            "number_of_projects": len(self.state['projects']),
            "projects": self.state['projects']
        }

    def fetch_user_repos(self, owner):
        """
        Récupère les dépôts pour un propriétaire donné.
        Args:
            owner (str): Nom du propriétaire du dépôt GitHub.
        Returns:
            list: Liste des dépôts.
        """
        repos = []
        page = 1
        while True:
            response = requests.get(f'https://api.github.com/users/{owner}/repos', headers=self.headers, params={'page': page, 'per_page': 100})
            if response.status_code == 200:
                repos_data = response.json()
                if not repos_data:
                    break
                repos.extend(repos_data)
                page += 1
            elif response.status_code == 403:
                print(f"Rate limit exceeded, sleeping for 60 seconds")
                time.sleep(60)
            else:
                print(f"Failed to fetch repos for {owner}: {response.status_code}")
                break
            
        return repos

    def fetch_repo(self, owner, repo_name):
        """
        Récupère les données d'un dépôt spécifique.
        Args:
            owner (str): Nom du propriétaire du dépôt GitHub.
            repo_name (str): Nom du dépôt.
        Returns:
            dict: Données du dépôt GitHub.
        """
        attempts = 3
        while attempts > 0:
            response = requests.get(f'https://api.github.com/repos/{owner}/{repo_name}', headers=self.headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403 and 'X-RateLimit-Reset' in response.headers:
                reset_time = int(response.headers['X-RateLimit-Reset'])
                sleep_time = max(reset_time - time.time(), 0) + 1
                print(f"Rate limit exceeded, sleeping for {sleep_time} seconds")
                time.sleep(sleep_time)
            else:
                print(f"Attempt to fetch repo {repo_name} failed: {response.status_code}")
                attempts -= 1
                time.sleep(1)  # Short sleep before retrying
        return None

    def fetch_repo_contributors(self, owner, repo_name):
        """
        Récupère les contributeurs d'un dépôt spécifique.
        Args:
            owner (str): Nom du propriétaire du dépôt GitHub.
            repo_name (str): Nom du dépôt.
        Returns:
            list: Liste des contributeurs avec leurs emails (si disponibles).
        """
        contributors = []
        response = requests.get(f'https://api.github.com/repos/{owner}/{repo_name}/contributors', headers=self.headers)
        if response.status_code == 200:
            contributors_data = response.json()
            for contributor in contributors_data:
                contributor_detail_response = requests.get(contributor['url'], headers=self.headers)
                if contributor_detail_response.status_code == 200:
                    contributor_detail = contributor_detail_response.json()
                    email = contributor_detail.get('email', 'Email not public')
                    contributors.append({
                        "name": contributor['login'],
                        "AuthGithubId": contributor['id'],
                        "email": email  # Only available if the user has made it public
                    })
                else:
                    contributors.append({
                        "name": contributor['login'],
                        "AuthGithubId": contributor['id'],
                        "email": "Failed to fetch email"
                    })
        return contributors

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

# Exemple d'utilisation
if __name__ == "__main__":
    input_filepath = 'CNRS_GITHUB_FROM_SH.json'  # Remplacez par le chemin de votre fichier JSON d'entrée
    output_filepath = 'CNRS_GITHUB_SH_OWNERS_REPOS.json'  # Remplacez par le chemin de votre fichier JSON de sortie
    github_api_token = 'YOUR_GITHUB_API_TOKEN_HERE'

    input_data = load_input_json(input_filepath)
    owners = {project['repo_info']['owner'] for project in input_data['projects'] if 'repo_info' in project}

    fetcher = GitHubRepoFetcher(github_api_token)
    try:
        output_data = fetcher.fetch_repos(owners)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        output_data = {"number_of_projects": 0, "projects": []}

    save_output_json(output_data, output_filepath)
    print(f"Les informations sur les projets ont été sauvegardées dans '{output_filepath}'.")

    # Suppression du fichier d'état après avoir terminé
    if os.path.exists(fetcher.state_file):
        os.remove(fetcher.state_file)
        print(f"Le fichier d'état '{fetcher.state_file}' a été supprimé.")
