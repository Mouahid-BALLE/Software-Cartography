import requests
import json
import time
import re

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
        Récupère les données d'un dépôt GitHub.
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
        try:
            response = requests.get(api_url, headers=self.headers)
            if response.status_code == 404:
                return None, "Repository not found"
            elif response.status_code == 403:
                return None, "Rate limit exceeded"
            response.raise_for_status()
            return response.json(), None
        except requests.exceptions.RequestException as e:
            return None, str(e)

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

    def collect_info(self, repo_data):
        """
        Collecte les informations pertinentes du dépôt GitHub.
        Args:
            repo_data (dict): Données du dépôt GitHub.
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
            "watchers": repo_data.get("watchers_count"),
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
            "repo_url": repo_data.get("html_url")
        }

    def process_projects(self, projects):
        """
        Traite les projets et récupère les informations des dépôts GitHub.
        Args:
            projects (list): Liste des projets.
        Returns:
            dict: Résultats avec les informations des dépôts GitHub.
        """

        results = {"projects": []}
        for project in projects:
            github_url = project.get("softCodeRepository") or project.get("softCodeRepository_sh")
            source_field = "softCodeRepository" if project.get("softCodeRepository") else "softCodeRepository_sh"

            if "github.com" not in github_url:
                results["projects"].append({
                    "project_number": project["project_number"],
                    "title": project["title"],
                    "repo_source": source_field,
                    "repo_url": github_url,
                    "error": "No valid GitHub URL found"
                })
                continue

            repo_data, error = self.fetch_repo_data(github_url)
            if error:
                if error == "Rate limit exceeded":
                    print("Rate limit exceeded, sleeping for 60 seconds")
                    time.sleep(60)
                    repo_data, error = self.fetch_repo_data(github_url)
                
                if error:
                    results["projects"].append({
                        "project_number": project["project_number"],
                        "title": project["title"],
                        "repo_source": source_field,
                        "repo_url": github_url,
                        "error": error
                    })
                    continue

            project_info = {
                "project_number": project["project_number"],
                "title": project["title"],
                "repo_source": source_field,
                "repo_url": github_url,
                "repo_info": self.collect_info(repo_data)
            }
            results["projects"].append(project_info)

        return results

    def save_json(self, data, filename):
        """
        Sauvegarde les données dans un fichier JSON.
        Args:
            data (dict): Données à sauvegarder.
            filename (str): Nom du fichier de sortie.
        """

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    """
    Fonction principale pour charger les projets, récupérer les informations GitHub, et sauvegarder les résultats.
    """
    # Charger les projets à partir d'un fichier JSON (METTRE LE BON CHEMIN VERS LE FICHIER CNRS_HAL)
    with open('../HAL/CNRS_HAL.json', 'r', encoding='utf-8') as f:
        projects_data = json.load(f)

    # Créer une instance de GitHubRepoInfoCollector avec votre jeton GitHub personnel
    github_collector = GitHubRepoInfoCollector(token="YOUR_GITHUB_TOKEN")

    # Traiter les projets et récupérer les informations GitHub
    results = github_collector.process_projects(projects_data["projects"])

    # Enregistrer les résultats dans un fichier JSON
    github_collector.save_json(results, 'CNRS_GITHUB.json')

if __name__ == "__main__":
    main()
