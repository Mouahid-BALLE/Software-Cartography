import json
import mysql.connector

def load_json_data(json_file):
    """
    Charge les données JSON à partir d'un fichier.

    Args:
        json_file (str): Chemin vers le fichier JSON.

    Returns:
        dict: Données JSON chargées.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_project_table(cursor):
    """
    Crée la table Project dans la base de données.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute('''CREATE TABLE IF NOT EXISTS Project
                      (Project_Id INT AUTO_INCREMENT PRIMARY KEY,
                       Hal_Id VARCHAR(255),
                       Title VARCHAR(255),
                       Abstract TEXT,
                       Date_creation VARCHAR(255),
                       Date_update VARCHAR(255),
                       Domain TEXT,
                       OnGithub BOOLEAN
                   )''')
    
def create_author_table(cursor):
    """
    Crée la table AUTHOR dans la base de données.
    
    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS AUTHOR (
            Author_Id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255),
            Hal_number_id VARCHAR(255),
            Hal_name_id VARCHAR(255)
        )
    """)

def create_forge_table(cursor):
    """
    Crée la table FORGE dans la base de données.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Forge (
            Forge_Id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255),
            Url VARCHAR(255)
        )
    """)

def create_lab_table(cursor):
    """
    Crée la table LAB dans la base de données.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Lab (
            Lab_Id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255)
        )
    """)

def create_keyword_table(cursor):
    """
    Crée la table KEYWORD dans la base de données.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Keyword (
            Keyword_Id INT AUTO_INCREMENT PRIMARY KEY,
            Label VARCHAR(255)
        )
    """)

def create_institution_table(cursor):
    """
    Crée la table INSTITUTION dans la base de données.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Institution (
            Institution_Id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255)
        )
    """)

def create_language_table(cursor):
    """
    Crée la table LANGUAGE dans la base de données.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Language (
            Language_Id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255) UNIQUE
        )
    """)

def create_source_table(cursor):
    """
    Crée la table SOURCE dans la base de données.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Source (
            Source_Id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255)
        )
    """)

def create_github_table(cursor):
    """
    Crée la table Github dans la base de données.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute('''CREATE TABLE Github
                      (Github_Id INT AUTO_INCREMENT PRIMARY KEY,
                       Name VARCHAR(255),
                       Full_Name VARCHAR(255),
                       Description TEXT,
                       Stars INT,
                       Forks INT,
                       Owner VARCHAR(255),
                       Watchers INT,
                       Open_Issues INT,
                       Contributors_Url VARCHAR(255),
                       Pulls_Url VARCHAR(255),
                       Commits_Url VARCHAR(255),
                       Releases_Url VARCHAR(255),
                       Language VARCHAR(255),
                       Created_At VARCHAR(255),
                       Updated_At VARCHAR(255),
                       Pushed_At VARCHAR(255),
                       Homepage VARCHAR(255),
                       Repo_Url VARCHAR(255))''')

def create_project_author_table(cursor):
    """
    Crée la table de liaison many-to-many entre les projets et les auteurs.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Project_Author (
            Project_Id INT,
            Author_Id INT,
            FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id) ON DELETE CASCADE,
            FOREIGN KEY (Author_Id) REFERENCES Author(Author_Id) ON DELETE CASCADE,
            PRIMARY KEY (Project_Id, Author_Id)
        )
    """)

def create_project_lab_table(cursor):
    """
    Crée la table de liaison many-to-many entre les projets et les laboratoires.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Project_Lab (
            Project_Id INT,
            Lab_id INT,
            FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id) ON DELETE CASCADE,
            FOREIGN KEY (Lab_id) REFERENCES Lab(Lab_Id) ON DELETE CASCADE,
            PRIMARY KEY (Project_Id, Lab_id)
        )
    """)

def create_project_forge_table(cursor):
    """
    Crée la table de liaison many-to-many entre les projets et les forges.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Project_Forge (
            Project_Id INT,
            Forge_id INT,
            FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id) ON DELETE CASCADE,
            FOREIGN KEY (Forge_id) REFERENCES Forge(Forge_Id) ON DELETE CASCADE,
            PRIMARY KEY (Project_Id, Forge_id)
        )
    """)

def create_project_keyword_table(cursor):
    """
    Crée la table de liaison many-to-many entre les projets et les mots-clés.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Project_Keyword (
            Project_Id INT,
            Keyword_id INT,
            FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id) ON DELETE CASCADE,
            FOREIGN KEY (Keyword_id) REFERENCES Keyword(Keyword_Id) ON DELETE CASCADE,
            PRIMARY KEY (Project_Id, Keyword_id)
        )
    """)

def create_project_language_table(cursor):
    """
    Crée la table de liaison many-to-many entre les projets et les languages.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Project_Language (
            Project_Id INT,
            Language_id INT,
            FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id) ON DELETE CASCADE,
            FOREIGN KEY (Language_id) REFERENCES Language(Language_Id) ON DELETE CASCADE,
            PRIMARY KEY (Project_Id, Language_id)
        )
    """)

def create_project_source_table(cursor):
    """
    Crée la table de liaison many-to-many entre les projets et les sources.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Project_Source (
            Project_Id INT,
            Source_id INT,
            FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id) ON DELETE CASCADE,
            FOREIGN KEY (Source_id) REFERENCES Source(Source_Id) ON DELETE CASCADE,
            PRIMARY KEY (Project_Id, Source_id)
        )
    """)

def create_project_github_table(cursor):
    """
    Crée la table de liaison entre Project et Github.
    
    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
    """
    cursor.execute('''CREATE TABLE Project_Github
                      (Project_Id INT,
                       Github_Id INT,
                       FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id),
                       FOREIGN KEY (Github_Id) REFERENCES Github(Github_Id),
                       PRIMARY KEY (Project_Id, Github_Id))''')

def insert_projects(cursor, projects, projects_github):
    """
    Insère les projets dans la table Project.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets à insérer.
        projects_github (list): Liste des projets GitHub contenant les informations supplémentaires.
    """
    for project in projects:
        hal_id = project.get('hal_id', '')
        title = project.get('title', '')
        abstract = project.get('abstract', '')
        date_creation = project.get('date', '')
        date_update = project.get('submitted_date', '')
        domain = project.get('domain', '')
        onGithub = True
        # Extraire le nombre d'étoiles du projet GitHub correspondant
        github_info = next((item for item in projects_github if item['title'] == title), None)

        #mettre onGithub à False si le projet n'est pas sur github
        stars = github_info.get('repo_info', {}).get('stars', "None")
        if stars != "None":
            onGithub = False

        # Requête SQL pour insérer les données
        insert_query = '''INSERT INTO Project 
                          (Hal_Id, Title, Abstract, Date_creation, Date_update, Domain, OnGithub) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(insert_query, (hal_id, title, abstract, date_creation, date_update, domain, onGithub))

        # Récupérer l'ID du projet inséré pour les relations many-to-many
        Project_Id = cursor.lastrowid
        project['Project_Id'] = Project_Id

def insert_authors(cursor, projects):
    """
    Insère les auteurs dans la table Author en évitant les doublons.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les auteurs à insérer.
    """
    author_set = set()  # Utilisé pour stocker les auteurs déjà insérés
    for project in projects:
        authors = project.get('authors', [])
        for author_info in authors:
            author_name = author_info.get('name', '')
            author_name_id = author_info.get('authIdHal_s', '')
            author_number_id= author_info.get('authIdHal_i', '')
            if author_name not in author_set:  # Vérifie si l'auteur n'a pas déjà été inséré
                cursor.execute("""
                    INSERT IGNORE INTO Author (Name, Hal_name_id, Hal_number_id) VALUES (%s, %s, %s)
                """, (author_name.strip(), author_name_id.strip(), author_number_id))
                author_set.add(author_name)  # Ajoute l'auteur à l'ensemble pour éviter les doublons

def insert_forges(cursor, projects):
    """
    Insère les forges dans la table Forge.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les informations sur les forges.
    """
    forge_set = set()  # Utilisé pour éviter les doublons
    for project in projects:
        url = project.get('softCodeRepository', '')
        if url:
            repo_site = url.split('//')[-1].split('/')[0]  # Extraire le nom de la forge
            if (repo_site, url) not in forge_set:
                cursor.execute("""
                    INSERT IGNORE INTO Forge (Name, Url) VALUES (%s, %s)
                """, (repo_site, url))
                forge_set.add((repo_site, url))  # Ajoute la forge à l'ensemble pour éviter les doublons

def insert_labs(cursor, projects):
    """
    Insère les laboratoires dans la table Lab.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les informations sur les laboratoires.
    """
    lab_set = set()  # Utilisé pour éviter les doublons
    for project in projects:
        laboratory = project.get('laboratory', '')
        if laboratory and laboratory not in lab_set:
            cursor.execute("""
                INSERT IGNORE INTO Lab (Name) VALUES (%s)
            """, (laboratory,))
            lab_set.add(laboratory)  # Ajoute le laboratoire à l'ensemble pour éviter les doublons

def insert_keywords(cursor, projects):
    """
    Insère les mots-clés dans la table Keyword.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les informations sur les mots-clés.
    """
    keyword_set = set()  # Utilisé pour éviter les doublons
    for project in projects:
        keywords = project.get('keywords', '').split(',')
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword and keyword not in keyword_set:
                cursor.execute("""
                    INSERT IGNORE INTO Keyword (Label) VALUES (%s)
                """, (keyword,))
                keyword_set.add(keyword)  # Ajoute le mot-clé à l'ensemble pour éviter les doublons

def insert_institutions(cursor, projects):
    """
    Insère les institutions dans la table Institution.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les informations sur les institutions.
    """
    institution_set = set()  # Utilisé pour éviter les doublons
    for project in projects:
        institution = project.get('structures', '')
        if institution and institution not in institution_set:
            cursor.execute("""
                INSERT IGNORE INTO Institution (Name) VALUES (%s)
            """, (institution,))
            institution_set.add(institution)  # Ajoute l'institution à l'ensemble pour éviter les doublons

def insert_languages(cursor, projects):
    """
    Insère les languages dans la table Language en évitant les doublons.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les informations sur les languages.
    """
    language_set = set()  # Utilisé pour éviter les doublons
    for project in projects:
        languages = project.get('softProgrammingLanguage', [])
        for language in languages:
            language = language.strip()
            if language and language not in language_set:
                cursor.execute("""
                    INSERT IGNORE INTO Language (Name) VALUES (%s)
                """, (language,))
                language_set.add(language)  # Ajoute le language à l'ensemble pour éviter les doublons

def insert_sources(cursor, projects):
    """
    Insère les sources dans la table Source.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les informations sur les sources.
    """
    source_set = set()  # Utilisé pour éviter les doublons
    for project in projects:
        source = project.get('source', '')
        if source and source not in source_set:
            cursor.execute("""
                INSERT IGNORE INTO Source (Name) VALUES (%s)
            """, (source,))
            source_set.add(source)  # Ajoute la source à l'ensemble pour éviter les doublons

def insert_github(cursor, projects):
    """
    Insère les projets GitHub dans la table Github.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets à insérer avec des informations GitHub.
    """
    for project in projects:
        repo_info = project.get('repo_info')
        if not repo_info:
            continue  # Ignorer les projets sans informations GitHub

        insert_query = '''INSERT INTO Github 
                          (Name, Full_Name, Description, Stars, Forks, Owner, Watchers, Open_Issues, 
                           Contributors_Url, Pulls_Url, Commits_Url, Releases_Url, Language, 
                           Created_At, Updated_At, Pushed_At, Homepage, Repo_Url) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(insert_query, (
            repo_info.get('name'),
            repo_info.get('full_name'),
            repo_info.get('description'),
            repo_info.get('stars'),
            repo_info.get('forks'),
            repo_info.get('owner'),
            repo_info.get('watchers'),
            repo_info.get('open_issues'),
            repo_info.get('contributors_url'),
            repo_info.get('pulls_url'),
            repo_info.get('commits_url'),
            repo_info.get('releases_url'),
            repo_info.get('language'),
            repo_info.get('created_at'),
            repo_info.get('updated_at'),
            repo_info.get('pushed_at'),
            repo_info.get('homepage'),
            repo_info.get('repo_url')
        ))

# Note: Cette fonction est appelée après avoir inséré les projets et les auteurs
def insert_project_authors(cursor, projects):
    """
    Insère la relation many-to-many entre les projets et les auteurs dans la table de liaison Project_Author.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les informations sur les auteurs.
    """
    for project in projects:
        
        cursor.execute("""
            SELECT Project_Id FROM Project WHERE Hal_Id = %s
        """, (project.get('hal_id', ''),))
        project_result = cursor.fetchone()
        cursor.fetchall()
        if project_result is None:
            print(f"Projet avec Hal_Id {project.get('hal_id', '')} non trouvé dans la table Project")
            continue
        Project_Id = project_result[0]

        authors = project.get('authors', [])
        for author_info in authors:
            author_name = author_info.get('name', '')
            
            # Récupérer l'ID de l'auteur depuis la table Author
            cursor.execute("""
                SELECT Author_Id FROM Author WHERE Name = %s
            """, (author_name.strip(),))
            author_result = cursor.fetchone()
            cursor.fetchall()
            if author_result is None:
                print(f"Auteur {author_name} non trouvé dans la table Author")
                continue

            Author_Id = author_result[0]

            # Insérer la relation many-to-many dans la table de liaison
            cursor.execute("""
                INSERT IGNORE INTO Project_Author (Project_Id, Author_Id) VALUES (%s, %s)
            """, (Project_Id, Author_Id))

def insert_project_labs(cursor, projects):
    """
    Insère la relation many-to-many entre les projets et les laboratoires dans la table de liaison Project_Lab.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les informations sur les laboratoires.
    """
    for project in projects:
        # Récupérer l'ID du projet depuis la table Project
        cursor.execute("""
            SELECT Project_Id FROM Project WHERE Hal_Id = %s
        """, (project.get('hal_id', ''),))
        project_result = cursor.fetchone()
        cursor.fetchall()
        if project_result is None:
            print(f"Projet avec Hal_Id {project.get('hal_id', '')} non trouvé dans la table Project")
            continue
        Project_Id = project_result[0]

        # Récupérer le laboratoire associé au projet
        lab_name = project.get('laboratory', '').strip()
        if lab_name:
            # Récupérer l'ID du laboratoire depuis la table Lab
            cursor.execute("""
                SELECT Lab_Id FROM Lab WHERE Name = %s
            """, (lab_name,))
            lab_result = cursor.fetchone()
            cursor.fetchall()
            if lab_result is None:
                print(f"Laboratoire {lab_name} non trouvé dans la table Lab")
                continue

            lab_id = lab_result[0]

            # Insérer la relation many-to-many dans la table de liaison
            cursor.execute("""
                INSERT IGNORE INTO Project_Lab (Project_Id, Lab_id) VALUES (%s, %s)
            """, (Project_Id, lab_id))

def insert_project_forges(cursor, projects):
    """
    Insère la relation many-to-many entre les projets et les forges dans la table de liaison Project_Forge.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les informations sur les forges.
    """
    for project in projects:
        # Récupérer l'ID du projet depuis la table Project
        cursor.execute("""
            SELECT Project_Id FROM Project WHERE Hal_Id = %s
        """, (project.get('hal_id', ''),))
        project_result = cursor.fetchone()
        cursor.fetchall()
        if project_result is None:
            print(f"Projet avec Hal_Id {project.get('hal_id', '')} non trouvé dans la table Project")
            continue
        Project_Id = project_result[0]

        # Récupérer l'URL du dépôt de code associé au projet
        url = project.get('softCodeRepository', '').strip()
        if url:
            repo_site = url.split('//')[-1].split('/')[0]  # Extraire le nom de la forge

            # Récupérer l'ID de la forge depuis la table Forge
            cursor.execute("""
                SELECT Forge_Id FROM Forge WHERE Name = %s
            """, (repo_site,))
            forge_result = cursor.fetchone()
            cursor.fetchall()
            if forge_result is None:
                print(f"Forge {repo_site} non trouvée dans la table Forge")
                continue
            forge_id = forge_result[0]

            # Insérer la relation many-to-many dans la table de liaison
            cursor.execute("""
                INSERT IGNORE INTO Project_Forge (Project_Id, Forge_id) VALUES (%s, %s)
            """, (Project_Id, forge_id))


def insert_project_keywords(cursor, projects):
    """
    Insère la relation many-to-many entre les projets et les mots-clés dans la table de liaison Project_Keyword.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les informations sur les mots-clés.
    """
    for project in projects:
        # Récupérer l'ID du projet depuis la table Project
        cursor.execute("""
            SELECT Project_Id FROM Project WHERE Hal_Id = %s
        """, (project.get('hal_id', ''),))
        project_result = cursor.fetchone()
        cursor.fetchall()
        if project_result is None:
            print(f"Projet avec Hal_Id {project.get('hal_id', '')} non trouvé dans la table Project")
            continue
        Project_Id = project_result[0]

        # Récupérer les mots-clés associés au projet
        keywords = project.get('keywords', '').split(',')
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword:
                # Récupérer l'ID du mot-clé depuis la table Keyword
                cursor.execute("""
                    SELECT Keyword_Id FROM Keyword WHERE Label = %s
                """, (keyword,))
                keyword_result = cursor.fetchone()
                cursor.fetchall()
                if keyword_result is None:
                    print(f"Mot-clé {keyword} non trouvé dans la table Keyword")
                    continue
                keyword_id = keyword_result[0]

                # Insérer la relation many-to-many dans la table de liaison
                cursor.execute("""
                    INSERT IGNORE INTO Project_Keyword (Project_Id, Keyword_id) VALUES (%s, %s)
                """, (Project_Id, keyword_id))

def insert_project_languages(cursor, projects):
    """
    Insère la relation many-to-many entre les projets et les languages dans la table de liaison Project_Language.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les informations sur les languages.
    """
    for project in projects:
        # Récupérer l'ID du projet depuis la table Project
        cursor.execute("""
            SELECT Project_Id FROM Project WHERE Hal_Id = %s
        """, (project.get('hal_id', ''),))
        project_result = cursor.fetchone()
        cursor.fetchall()
        if project_result is None:
            print(f"Projet avec Hal_Id {project.get('hal_id', '')} non trouvé dans la table Project")
            continue
        Project_Id = project_result[0]

        languages = project.get('softProgrammingLanguage', [])
        for language in languages:
            language = language.strip()
            
            # Récupérer l'ID du language depuis la table Language
            cursor.execute("""
                SELECT Language_Id FROM Language WHERE Name = %s
            """, (language,))
            language_result = cursor.fetchone()
            cursor.fetchall()
            if language_result is None:
                print(f"Langage {language} non trouvé dans la table Language")
                continue

            language_id = language_result[0]

            # Insérer la relation many-to-many dans la table de liaison
            cursor.execute("""
                INSERT IGNORE INTO Project_Language (Project_Id, Language_id) VALUES (%s, %s)
            """, (Project_Id, language_id))

def insert_project_sources(cursor, projects):
    """
    Insère la relation many-to-many entre les projets et les sources dans la table de liaison Project_Source.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les informations sur les sources.
    """
    for project in projects:
        # Récupérer l'ID du projet depuis la table Project
        cursor.execute("""
            SELECT Project_Id FROM Project WHERE Hal_Id = %s
        """, (project.get('hal_id', ''),))
        project_result = cursor.fetchone()
        cursor.fetchall()
        if project_result is None:
            print(f"Projet avec Hal_Id {project.get('hal_id', '')} non trouvé dans la table Project")
            continue
        Project_Id = project_result[0]

        source = project.get('source', '').strip()
        if source:
            # Récupérer l'ID de la source depuis la table Source
            cursor.execute("""
                SELECT Source_Id FROM Source WHERE Name = %s
            """, (source,))
            source_result = cursor.fetchone()
            cursor.fetchall()
            if source_result is None:
                print(f"Source {source} non trouvée dans la table Source")
                continue
            source_id = source_result[0]

            # Insérer la relation many-to-many dans la table de liaison
            cursor.execute("""
                INSERT IGNORE INTO Project_Source (Project_Id, Source_id) VALUES (%s, %s)
            """, (Project_Id, source_id))

def insert_project_github_relations(cursor, projects, projects_github):
    """
    Insère les relations entre les projets et leurs informations GitHub dans la table de liaison.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        projects (list): Liste des projets contenant les relations à insérer.
        projects_github (list): Liste des projets GitHub contenant les informations supplémentaires.
    """
    for project in projects:
        title = project.get('title')

        # Récupérer l'ID du projet depuis la table Project
        cursor.execute("SELECT Project_Id FROM Project WHERE Title = %s", (title,))
        project_result = cursor.fetchone()
        cursor.fetchall()
        if not project_result:
            #print(f"Projet '{title}' non trouvé dans la table Project.")
            continue
        project_id = project_result[0]

        # Récupérer l'ID du projet GitHub depuis la table Github
        github_info = next((item for item in projects_github if item['title'] == title), None)
        if not github_info or 'repo_info' not in github_info:
            #print(f"Projet GitHub pour '{title}' non trouvé ou sans informations dans les projets GitHub.")
            continue

        cursor.execute("SELECT Github_Id FROM Github WHERE Full_Name = %s", (github_info['repo_info']['full_name'],))
        github_result = cursor.fetchone()
        cursor.fetchall()
        if not github_result:
            #print(f"Dépôt GitHub '{github_info['repo_info']['full_name']}' non trouvé dans la table Github.")
            continue
        github_id = github_result[0]

        # Insérer la relation dans la table de liaison Project_Github
        insert_query = '''INSERT IGNORE INTO Project_Github (Project_Id, Github_Id) VALUES (%s, %s)'''
        cursor.execute(insert_query, (project_id, github_id))

def create_database(cursor, db_name):
    """
    Crée la base de données si elle n'existe pas.

    Args:
        cursor: Curseur MySQL pour exécuter les requêtes SQL.
        db_name (str): Nom de la base de données.
    """
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")
    print("Base de données créée avec succès.")

def drop_database_if_exists(db_config, db_name):
    """
    Supprime la base de données spécifiée.

    Args:
        db_config (dict): Configuration de la base de données MySQL.
        db_name (str): Nom de la base de données à supprimer.
    """
    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()
        
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        print(f"La base de données '{db_name}' a été supprimée avec succès.")
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Erreur : {err}")

def fill_database(projects,project_github, db_config):
    """
    Crée la base de données MySQL et insère les données des projets.

    Args:
        projects (list): Liste des projets contenant les données à insérer.
        db_config (dict): Configuration de la base de données MySQL.
    """
    drop_database_if_exists(db_config, db_config['database'])
    
    # Connexion sans spécifier de base de données pour vérifier si la base existe ou créer la base de données
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password']
    )
    cursor = conn.cursor()

    # Créer la base de données si elle n'existe pas
    create_database(cursor, db_config['database'])

    # Fermer la connexion initiale et reconnecter
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    create_project_table(cursor)
    insert_projects(cursor, projects, project_github)

    create_author_table(cursor)
    insert_authors(cursor, projects)

    create_forge_table(cursor)
    insert_forges(cursor, projects)

    create_lab_table(cursor)
    insert_labs(cursor, projects)

    create_keyword_table(cursor)
    insert_keywords(cursor, projects)

    create_institution_table(cursor)
    insert_institutions(cursor, projects)

    create_language_table(cursor)
    insert_languages(cursor, projects)

    create_source_table(cursor)
    insert_sources(cursor, projects)

    create_github_table(cursor)
    insert_github(cursor, project_github)

    create_project_author_table(cursor)
    insert_project_authors(cursor, projects)

    create_project_lab_table(cursor) 
    insert_project_labs(cursor, projects)

    create_project_forge_table(cursor)
    insert_project_forges(cursor, projects)

    create_project_keyword_table(cursor)
    insert_project_keywords(cursor, projects)

    create_project_language_table(cursor)
    insert_project_languages(cursor, projects)

    create_project_source_table(cursor)
    insert_project_sources(cursor, projects)

    create_project_github_table(cursor)
    insert_project_github_relations(cursor, projects, project_github)

    conn.commit()
    cursor.close()
    conn.close()

    print("Données insérées avec succès dans la base de données.")

def main():
    json_file_hal = 'CNRS_HAL.json' 
    json_file_github = '../Git/CNRS_GITHUB.json'
    db_config = {
        'host': 'localhost',
        'user': 'mouahid',
        'password': 'MdpSQL',
        'database': 'cnrs_hal_db'
    }
    data_hal = load_json_data(json_file_hal)
    projects = data_hal.get('projects', [])

    data_github = load_json_data(json_file_github)
    projects_github = data_github.get('projects', []) 

    fill_database(projects,projects_github, db_config)


if __name__ == '__main__':
    main()
    
