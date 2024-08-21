import mysql.connector
import pandas as pd

"""
Description : Ce script est conçu pour se connecter à une base de données MySQL, récupérer des informations
sur des projets GitHub et GitLab stockées dans la base de données, et exporter ces informations dans des fichiers CSV. 
Il permet de centraliser la gestion des opérations liées à la base de données, telles que l'exécution de requêtes SQL, 
le traitement des résultats, et leur sauvegarde dans des fichiers pour une analyse ou une utilisation ultérieure.

Entrées :
- `db_config` : Dictionnaire contenant les paramètres de connexion à la base de données MySQL, tels que l'hôte, 
l'utilisateur, le mot de passe, et le nom de la base de données.

Sorties :
- `github_projects.csv` : Fichier CSV contenant les informations des projets GitHub extraites de la base de données.
- `gitlab_projects.csv` : Fichier CSV contenant les informations des projets GitLab extraites de la base de données.
"""

class CSVManager:
    def __init__(self, db_config):
        """
        Initialise la classe avec les configurations de la base de données.
        Args:
            db_config (dict): Dictionnaire contenant les paramètres de connexion à la base de données.
        """
        self.db_config = db_config
        self.conn = None  # La connexion à la base de données sera stockée ici
        self.cursor = None  # Le curseur pour exécuter les requêtes sera stocké ici

    def connect(self):
        """
        Établit la connexion à la base de données en utilisant les paramètres fournis.
        """
        self.conn = mysql.connector.connect(**self.db_config)  # Connexion à la base de données
        self.cursor = self.conn.cursor(dictionary=True)  # Création d'un curseur qui retourne les résultats sous forme de dictionnaire

    def close(self):
        """
        Ferme la connexion à la base de données et le curseur.
        """
        if self.cursor:
            self.cursor.close()  # Ferme le curseur s'il est ouvert
        if self.conn:
            self.conn.close()  # Ferme la connexion s'il est ouvert

    def execute_query(self, query):
        """
        Exécute une requête SQL et retourne les résultats.
        Args:
            query (str): La requête SQL à exécuter.
        Returns:
            list: Liste des résultats sous forme de dictionnaires.
        """
        self.cursor.execute(query)  # Exécution de la requête SQL
        return self.cursor.fetchall()  # Récupération de tous les résultats

    def fetch_github_projects(self):
        """
        Récupère les informations des projets GitHub depuis la base de données.
        Returns:
            list: Liste des projets GitHub, chaque projet étant représenté par un dictionnaire.
        """
        query = """
        SELECT 
            g.Name AS Project_Name,
            g.Stars AS Stars,
            g.Forks AS Forks,
            g.Subscribers AS Subscribers,
            g.Open_Issues AS Open_Issues,
            g.Created_At AS Created_At,
            g.Updated_At AS Updated_At,
            g.Pushed_At AS Pushed_At,
            g.Size AS Size,
            g.Archived AS Archived,
            g.Has_Projects AS Has_Projects,
            g.Has_Downloads AS Has_Downloads,
            g.Has_Wiki AS Has_Wiki,
            g.Homepage AS Homepage,
            g.Repo_Url AS URL,
            g.Commits AS Commits
        FROM 
            Github g
        JOIN 
            Project_Github pg ON g.Github_Id = pg.Github_Id
        JOIN 
            Project p ON pg.Project_Id = p.Project_Id
        """  # Requête SQL pour récupérer les informations des projets GitHub
        results = self.execute_query(query)  # Exécution de la requête
        unique_results = {project['URL']: project for project in results}.values()  # Élimination des doublons par URL
        return list(unique_results)  # Retourne les projets sous forme de liste

    def fetch_gitlab_projects(self):
        """
        Récupère les informations des projets GitLab depuis la base de données.
        Returns:
            list: Liste des projets GitLab, chaque projet étant représenté par un dictionnaire.
        """
        query = """
        SELECT 
            gl.Name AS Project_Name,
            p.url AS URL,
            gl.Stars AS Stars,
            gl.Forks AS Forks,
            CASE 
                WHEN gl.Readme IS NOT NULL AND gl.Readme <> '' THEN 'Yes'
                ELSE 'No'
            END AS Has_Readme
        FROM 
            Gitlab gl
        JOIN 
            Project_Gitlab pg ON gl.Gitlab_Id = pg.Gitlab_Id
        JOIN 
            Project p ON pg.Project_Id = p.Project_Id
        """  # Requête SQL pour récupérer les informations des projets GitLab
        results = self.execute_query(query)  # Exécution de la requête
        unique_results = {project['URL']: project for project in results}.values()  # Élimination des doublons par URL
        return list(unique_results)  # Retourne les projets sous forme de liste

    def write_github_projects_to_csv(self, filename):
        """
        Écrit les informations des projets GitHub dans un fichier CSV.
        Args:
            filename (str): Le nom du fichier CSV de sortie.
        """
        projects = self.fetch_github_projects()  # Récupère les projets GitHub depuis la base de données
        df = pd.DataFrame(projects)  # Convertit les projets en DataFrame pandas
        df.to_csv(filename, index=False, encoding='utf-8')  # Sauvegarde les données dans un fichier CSV
        print(f"Les informations des projets GitHub ont été écrites dans le fichier '{filename}'.")

    def write_gitlab_projects_to_csv(self, filename):
        """
        Écrit les informations des projets GitLab dans un fichier CSV.
        Args:
            filename (str): Le nom du fichier CSV de sortie.
        """
        projects = self.fetch_gitlab_projects()  # Récupère les projets GitLab depuis la base de données
        df = pd.DataFrame(projects)  # Convertit les projets en DataFrame pandas
        df.to_csv(filename, index=False, encoding='utf-8')  # Sauvegarde les données dans un fichier CSV
        print(f"Les informations des projets GitLab ont été écrites dans le fichier '{filename}'.")

def main():
    """
    Fonction principale pour gérer la connexion à la base de données, récupérer les projets GitHub et GitLab, et les écrire dans des fichiers CSV.
    """
    db_config = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'cnrs_db'
    }
    
    csv_manager = CSVManager(db_config)  # Création d'une instance de CSVManager
    csv_manager.connect()  # Connexion à la base de données
    
    csv_manager.write_github_projects_to_csv('github_projects.csv')  # Écriture des projets GitHub dans un CSV
    csv_manager.write_gitlab_projects_to_csv('gitlab_projects.csv')  # Écriture des projets GitLab dans un CSV
    
    csv_manager.close()  # Fermeture de la connexion à la base de données

if __name__ == "__main__":
    main()  # Exécution de la fonction principale
