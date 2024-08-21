import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

"""
Description : Ce script se connecte à une base de données MySQL, récupère des informations spécifiques 
sur les projets GitHub et GitLab, ainsi que sur les langages de programmation, les sources de projets, 
les forges, et les laboratoires associés. Les données extraites sont ensuite utilisées pour générer des 
graphiques, permettant de visualiser les projets les plus étoilés, la distribution des projets par source, 
les forges les plus populaires, et d'autres statistiques pertinentes. Ces graphiques sont sauvegardés sous 
forme de fichiers image pour une analyse ultérieure.

Entrées :
- `db_config` : Dictionnaire contenant les paramètres de connexion à la base de données (hôte, utilisateur
, mot de passe, et nom de la base de données).

Sorties :
- `top_starred_projects_github.png` : Graphique des 5 projets GitHub les plus étoilés.
- `top_starred_projects_gitlab.png` : Graphique des 5 projets GitLab les plus étoilés.
- `projects_by_source.png` : Graphique en secteurs montrant la répartition des projets par source.
- `top_forges.png` : Graphique des 10 forges avec le plus de projets.
- `projects_with_homepage_github.png` : Graphique en secteurs montrant la proportion de projets GitHub ayant une homepage.
- `top_languages_github.png` : Graphique des 10 langages les plus utilisés sur GitHub.
- `top_labs_by_contributions.png` : Graphique des 30 laboratoires avec le plus de contributions.
"""


class DatabaseManager:
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

    def fetch_top_starred_projects_github(self):
        """
        Récupère les 5 projets les plus étoilés sur GitHub.
        Returns:
            list: Liste des projets GitHub les plus étoilés, chaque projet étant représenté par un dictionnaire.
        """
        query = "SELECT Name, Stars FROM Github ORDER BY Stars DESC LIMIT 5"
        return self.execute_query(query)

    def fetch_top_starred_projects_gitlab(self):
        """
        Récupère les 5 projets les plus étoilés sur GitLab.
        Returns:
            list: Liste des projets GitLab les plus étoilés, chaque projet étant représenté par un dictionnaire.
        """
        query = "SELECT Name, Stars FROM Gitlab ORDER BY Stars DESC LIMIT 5"
        return self.execute_query(query)

    def fetch_projects_by_source(self):
        """
        Récupère le nombre de projets par source.
        Returns:
            list: Liste des sources avec le nombre de projets associés.
        """
        query = """
        SELECT s.Name AS Source, COUNT(*) as count 
        FROM Source s
        JOIN Project_Source ps ON s.Source_Id = ps.Source_Id
        GROUP BY s.Name
        """
        return self.execute_query(query)

    def fetch_top_forges(self):
        """
        Récupère les 10 forges avec le plus de projets.
        Returns:
            list: Liste des forges avec le nombre de projets associés, triées par ordre décroissant.
        """
        query = """
        SELECT f.Name, COUNT(*) as count 
        FROM Forge f
        JOIN Project_Forge pf ON f.Forge_Id = pf.Forge_Id
        GROUP BY f.Name
        ORDER BY count DESC
        LIMIT 10
        """
        return self.execute_query(query)

    def fetch_projects_with_homepage_github(self):
        """
        Récupère le nombre de projets GitHub ayant une page d'accueil (homepage).
        Returns:
            list: Liste contenant un dictionnaire avec le nombre de projets ayant une homepage.
        """
        query = "SELECT COUNT(*) as count FROM Github WHERE Homepage IS NOT NULL AND Homepage <> ''"
        return self.execute_query(query)

    def fetch_total_projects_github(self):
        """
        Récupère le nombre total de projets GitHub.
        Returns:
            list: Liste contenant un dictionnaire avec le nombre total de projets.
        """
        query = "SELECT COUNT(*) as count FROM Github"
        return self.execute_query(query)

    def fetch_top_languages_github(self):
        """
        Récupère les 10 langages les plus utilisés sur GitHub.
        Returns:
            list: Liste des langages les plus utilisés, avec le nombre de projets associés.
        """
        query = """
        SELECT l.Name AS Language, COUNT(*) as count 
        FROM Language l
        JOIN Project_Language pl ON l.Language_Id = pl.Language_Id
        JOIN Project p ON pl.Project_Id = p.Project_Id
        GROUP BY l.Name
        ORDER BY count DESC
        LIMIT 10
        """
        return self.execute_query(query)

    def fetch_top_labs_by_contributions(self):
        """
        Récupère les 30 laboratoires ayant le plus de contributions.
        Returns:
            list: Liste des laboratoires avec le nombre de contributions, triées par ordre décroissant.
        """
        query = """
        SELECT l.Name AS Lab, COUNT(*) as count
        FROM Lab l
        JOIN Project_Lab pl ON l.Lab_Id = pl.Lab_Id
        GROUP BY l.Name
        ORDER BY count DESC
        LIMIT 30
        """
        return self.execute_query(query)

def plot_top_starred_projects_github(data):
    """
    Génère un graphique des 5 projets les plus étoilés sur GitHub.
    Args:
        data (list): Liste des projets GitHub avec leur nombre d'étoiles.
    """
    df = pd.DataFrame(data)  # Conversion des données en DataFrame
    df.plot(kind='bar', x='Name', y='Stars', legend=False)  # Création du graphique
    plt.title('Top 5 des projets les plus étoilés sur GitHub')  # Titre du graphique
    plt.ylabel('Étoiles')  # Légende de l'axe y
    plt.xlabel('Projet')  # Légende de l'axe x
    plt.tight_layout()  # Ajustement de la mise en page
    plt.savefig('top_starred_projects_github.png')  # Sauvegarde du graphique
    plt.show()  # Affichage du graphique

def plot_top_starred_projects_gitlab(data):
    """
    Génère un graphique des 5 projets les plus étoilés sur GitLab.
    Args:
        data (list): Liste des projets GitLab avec leur nombre d'étoiles.
    """
    df = pd.DataFrame(data)  # Conversion des données en DataFrame
    df.plot(kind='bar', x='Name', y='Stars', legend=False)  # Création du graphique
    plt.title('Top 5 des projets les plus étoilés sur GitLab')  # Titre du graphique
    plt.ylabel('Étoiles')  # Légende de l'axe y
    plt.xlabel('Projet')  # Légende de l'axe x
    plt.tight_layout()  # Ajustement de la mise en page
    plt.savefig('top_starred_projects_gitlab.png')  # Sauvegarde du graphique
    plt.show()  # Affichage du graphique

def plot_projects_by_source(data):
    """
    Génère un graphique en secteurs montrant la répartition des projets par source.
    Args:
        data (list): Liste des sources avec le nombre de projets associés.
    """
    df = pd.DataFrame(data)  # Conversion des données en DataFrame
    df.plot(kind='pie', y='count', labels=df['Source'], autopct='%1.1f%%', legend=False)  # Création du graphique en secteurs
    plt.title('Nombre de projets par source')  # Titre du graphique
    plt.tight_layout()  # Ajustement de la mise en page
    plt.savefig('projects_by_source.png')  # Sauvegarde du graphique
    plt.show()  # Affichage du graphique

def plot_top_forges(data):
    """
    Génère un graphique des 10 forges avec le plus de projets.
    Args:
        data (list): Liste des forges avec le nombre de projets associés.
    """
    df = pd.DataFrame(data)  # Conversion des données en DataFrame
    df.plot(kind='bar', x='Name', y='count', legend=False)  # Création du graphique
    plt.title('Top 10 des forges avec le plus de projets')  # Titre du graphique
    plt.ylabel('Nombre de projets')  # Légende de l'axe y
    plt.xlabel('Forge')  # Légende de l'axe x
    plt.tight_layout()  # Ajustement de la mise en page
    plt.savefig('top_forges.png')  # Sauvegarde du graphique
    plt.show()  # Affichage du graphique

def plot_projects_with_homepage_github(data, total_projects):
    """
    Génère un graphique en secteurs montrant la proportion de projets GitHub ayant une homepage.
    Args:
        data (list): Liste contenant le nombre de projets GitHub avec une homepage.
        total_projects (list): Liste contenant le nombre total de projets GitHub.
    """
    with_homepage = data[0]['count']  # Nombre de projets avec homepage
    without_homepage = total_projects[0]['count'] - with_homepage  # Nombre de projets sans homepage
    labels = ['With Homepage', 'Without Homepage']  # Légendes des secteurs
    sizes = [with_homepage, without_homepage]  # Tailles des secteurs
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')  # Création du graphique en secteurs
    plt.title('Projets GitHub avec une homepage')  # Titre du graphique
    plt.tight_layout()  # Ajustement de la mise en page
    plt.savefig('projects_with_homepage_github.png')  # Sauvegarde du graphique
    plt.show()  # Affichage du graphique

def plot_top_languages_github(data):
    """
    Génère un graphique des 10 langages les plus utilisés sur GitHub.
    Args:
        data (list): Liste des langages avec le nombre de projets associés.
    """
    df = pd.DataFrame(data)  # Conversion des données en DataFrame
    total = df['count'].sum()  # Calcul du total des projets
    df['percentage'] = (df['count'] / total) * 100  # Calcul du pourcentage pour chaque langage
    df.plot(kind='bar', x='Language', y='percentage', legend=False)  # Création du graphique
    plt.title('Top 10 des langages les plus utilisés sur GitHub')  # Titre du graphique
    plt.ylabel('Pourcentage')  # Légende de l'axe y
    plt.xlabel('Langage')  # Légende de l'axe x
    plt.tight_layout()  # Ajustement de la mise en page
    plt.savefig('top_languages_github.png')  # Sauvegarde du graphique
    plt.show()  # Affichage du graphique

def plot_top_labs_by_contributions(data):
    """
    Génère un graphique des 30 laboratoires ayant le plus de contributions.
    Args:
        data (list): Liste des laboratoires avec le nombre de contributions associées.
    """
    df = pd.DataFrame(data)  # Conversion des données en DataFrame
    df.plot(kind='bar', x='Lab', y='count', legend=False)  # Création du graphique
    plt.title('Top 30 des labos avec le plus de contributions')  # Titre du graphique
    plt.ylabel('Nombre de contributions')  # Légende de l'axe y
    plt.xlabel('Labo')  # Légende de l'axe x
    plt.tight_layout()  # Ajustement de la mise en page
    plt.savefig('top_labs_by_contributions.png')  # Sauvegarde du graphique
    plt.show()  # Affichage du graphique

def main():
    """
    Fonction principale pour gérer la connexion à la base de données, récupérer les données des projets,
    et générer des graphiques basés sur ces données.
    """
    db_config = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'cnrs_db'
    }
    db_manager = DatabaseManager(db_config)  # Création d'une instance de DatabaseManager
    db_manager.connect()  # Connexion à la base de données

    # Récupération des données depuis la base de données
    top_starred_projects_github = db_manager.fetch_top_starred_projects_github()
    top_starred_projects_gitlab = db_manager.fetch_top_starred_projects_gitlab()
    projects_by_source = db_manager.fetch_projects_by_source()
    top_forges = db_manager.fetch_top_forges()
    projects_with_homepage_github = db_manager.fetch_projects_with_homepage_github()
    total_projects_github = db_manager.fetch_total_projects_github()
    top_languages_github = db_manager.fetch_top_languages_github()
    top_labs_by_contributions = db_manager.fetch_top_labs_by_contributions()

    db_manager.close()  # Fermeture de la connexion à la base de données

    # Génération des graphiques basés sur les données récupérées
    plot_top_starred_projects_github(top_starred_projects_github)
    plot_top_starred_projects_gitlab(top_starred_projects_gitlab)
    plot_projects_by_source(projects_by_source)
    plot_top_forges(top_forges)
    plot_projects_with_homepage_github(projects_with_homepage_github, total_projects_github)
    plot_top_languages_github(top_languages_github)
    plot_top_labs_by_contributions(top_labs_by_contributions)

if __name__ == "__main__":
    main()  # Exécution de la fonction principale
