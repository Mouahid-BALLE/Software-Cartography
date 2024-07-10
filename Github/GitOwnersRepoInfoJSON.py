import requests
import json
import re
import os

""" A partir du fichier généré par GitOwnersRepoJSON.py, on va extraire les URLs des dépôts GitHub et récupérer les informations de ces dépôts."""

class GitHubRepoInfoCollector:
    def __init__(self, token):
        """
        Initialise la classe avec un jeton d'authentification GitHub.
        Args:
            token (str): Jeton d'authentification GitHub.
        """
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def fetch_repo_data(self, repo_url):
        """
        Récupère les données d'un dépôt GitHub à partir de son URL.
        Args:
            repo_url (str): URL du dépôt GitHub.
        Returns:
            dict: Données du dépôt GitHub.
            str: Message d'erreur, s'il y en a un.
        """
        repo_name = self.extract_repo_name(repo_url)
        if not repo_name:
            return None, "Invalid GitHub URL"

        api_url = f"https://api.github.com/repos/{repo_name}"
        response = requests.get(api_url, headers=self.headers)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, "Failed to fetch repo"

    def fetch_commit_count(self, repo_name):
        """
        Récupère le nombre de commits d'un dépôt GitHub.
        Args:
            repo_name (str): Nom du dépôt GitHub.
        Returns:
            int: Nombre de commits.
        """
        api_url = f"https://api.github.com/repos/{repo_name}/commits"
        response = requests.get(api_url, headers=self.headers, params={'per_page': 1})
        if response.status_code == 200:
            if 'Link' in response.headers:
                last_page_link = [link for link in response.headers['Link'].split(',') if 'rel="last"' in link]
                if last_page_link:
                    last_page_url = last_page_link[0].split(';')[0].strip('<> ')
                    num_commits = int(last_page_url.split('page=')[-1])
                    return num_commits
            return len(response.json())
        return 0

    def extract_repo_name(self, url):
        """
        Extrait le nom du dépôt GitHub à partir de l'URL.
        Args:
            url (str): URL du dépôt GitHub.
        Returns:
            str: Nom du dépôt GitHub.
        """
        match = re.search(r'github\.com/([^/]+/[^/]+)', url)
        return match.group(1) if match else None

    def collect_info(self, repo_data, commit_count):
        """
        Collecte les informations pertinentes d'un dépôt GitHub.
        Args:
            repo_data (dict): Données du dépôt GitHub.
            commit_count (int): Nombre de commits du dépôt.
        Returns:
            dict: Informations collectées.
        """
        return {
            "name": repo_data.get("name"),
            "full_name": repo_data.get("full_name"),
            "description": repo_data.get("description"),
            "stars": repo_data.get("stargazers_count"),
            "forks": repo_data.get("forks_count"),
            "owner": repo_data.get("owner").get("login"),
            "subscribers": repo_data.get("subscribers_count"),
            "open_issues": repo_data.get("open_issues_count"),
            "contributors_url": repo_data.get("contributors_url"),
            "pulls_url": repo_data.get("pulls_url"),
            "commits_url": repo_data.get("commits_url"),
            "releases_url": repo_data.get("releases_url"),
            "language": repo_data.get("language"),
            "created_at": repo_data.get("created_at"),
            "updated_at": repo_data.get("updated_at"),
            "pushed_at": repo_data.get("pushed_at"),
            "homepage": repo_data.get("homepage"),
            "repo_url": repo_data.get("html_url"),
            "commit_count": commit_count
        }

    def process_project(self, project):
        """
        Traite un projet et récupère les informations du dépôt GitHub associé.
        Args:
            project (dict): Données du projet.
        Returns:
            dict: Résultats avec les informations du dépôt GitHub.
        """
        github_url = project.get("softCodeRepository")

        repo_data, error = self.fetch_repo_data(github_url)
        if error:
            return {
                "project_number": project["project_number"],
                "title": project["title"],
                "repo_source": "softCodeRepository",
                "repo_url": github_url,
                "error": error
            }

        repo_name = self.extract_repo_name(github_url)
        commit_count = self.fetch_commit_count(repo_name)

        return {
            "project_number": project["project_number"],
            "title": project["title"],
            "repo_source": "softCodeRepository",
            "repo_url": github_url,
            "repo_info": self.collect_info(repo_data, commit_count)
        }

    def save_json(self, data, filename):
        """
        Sauvegarde les données dans un fichier JSON.
        Args:
            data (dict): Données à sauvegarder.
            filename (str): Nom du fichier de sortie.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def load_state(state_file):
    """
    Charge l'état à partir du fichier d'état.
    Args:
        state_file (str): Chemin vers le fichier d'état.
    Returns:
        dict: État chargé.
    """
    if os.path.exists(state_file):
        with open(state_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"last_processed_index": -1, "results": []}

def save_state(state, state_file):
    """
    Sauvegarde l'état dans un fichier.
    Args:
        state (dict): État à sauvegarder.
        state_file (str): Chemin vers le fichier de sortie.
    """
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=4)

def main():
    """
    Fonction principale pour charger les projets, récupérer les informations GitHub, et sauvegarder les résultats.
    """
    input_filepath = 'CNRS_GITHUB_HAL_OWNERS_REPOS.json'
    output_filepath = 'CNRS_GITHUB_HAL_OWNERS_REPOS_INFO.json'
    state_filepath = 'owner_info_state.json'

    with open(input_filepath, 'r', encoding='utf-8') as f:
        projects_data = json.load(f)

    github_collector = GitHubRepoInfoCollector(token="YOUR_GITHUB_API_TOKEN_HERE")
    state = load_state(state_filepath)
    last_processed_index = state["last_processed_index"]
    results = state["results"]

    for index in range(last_processed_index + 1, len(projects_data["projects"])):
        project = projects_data["projects"][index]
        result = github_collector.process_project(project)
        results.append(result)

        # Mise à jour de l'état
        state["last_processed_index"] = index
        state["results"] = results
        save_state(state, state_filepath)

    # Sauvegarder les résultats finaux
    github_collector.save_json({"projects": results}, output_filepath)

    # Suppression du fichier d'état après avoir terminé
    if os.path.exists(state_filepath):
        os.remove(state_filepath)

if __name__ == "__main__":
    main()
