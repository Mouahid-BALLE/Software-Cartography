import json
import mysql.connector

class DatabaseManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = mysql.connector.connect(**self.db_config)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def load_json_data(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    
    def create_project_table(self):
        """
        Crée la table Project dans la base de données.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Project
                        (Project_Id INT AUTO_INCREMENT PRIMARY KEY,
                        Title VARCHAR(255),
                        Abstract TEXT,
                        Date_creation VARCHAR(255),
                        Date_update VARCHAR(255),
                        Domain TEXT,
                        Url TEXT,
                        OnGithub BOOLEAN
                    )''')

    def create_author_table(self):
        """
        Crée la table AUTHOR dans la base de données.
        
        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS AUTHOR (
                Author_Id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255),
                Mail VARCHAR(255),
                Hal_number_id VARCHAR(255),
                Hal_name_id VARCHAR(255),
                Github_id VARCHAR(255)
            )
        """)

    def create_forge_table(self):
        """
        Crée la table FORGE dans la base de données.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Forge (
                Forge_Id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255)
            )
        """)

    def create_lab_table(self):
        """
        Crée la table LAB dans la base de données.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Lab (
                Lab_Id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255)
            )
        """)

    def create_keyword_table(self):
        """
        Crée la table KEYWORD dans la base de données.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Keyword (
                Keyword_Id INT AUTO_INCREMENT PRIMARY KEY,
                Label VARCHAR(255)
            )
        """)

    def create_institution_table(self):
        """
        Crée la table INSTITUTION dans la base de données.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Institution (
                Institution_Id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255)
            )
        """)

    def create_language_table(self):
        """
        Crée la table LANGUAGE dans la base de données.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Language (
                Language_Id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) UNIQUE
            )
        """)

    def create_source_table(self):
        """
        Crée la table SOURCE dans la base de données.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Source (
                Source_Id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255),
                Hal_id VARCHAR(255),
                Github_id VARCHAR(255),
                Sh_id VARCHAR(255)
            )
        """)

    def create_github_table(self):
        """
        Crée la table Github dans la base de données.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute('''CREATE TABLE Github
                        (Github_Id INT AUTO_INCREMENT PRIMARY KEY,
                        Name VARCHAR(255),
                        Full_Name VARCHAR(255),
                        Description TEXT,
                        Stars INT,
                        Forks INT,
                        Owner VARCHAR(255),
                        Subscribers INT,
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

    def create_project_author_table(self):
        """
        Crée la table de liaison many-to-many entre les projets et les auteurs.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Project_Author (
                Project_Id INT,
                Author_Id INT,
                FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id) ON DELETE CASCADE,
                FOREIGN KEY (Author_Id) REFERENCES Author(Author_Id) ON DELETE CASCADE,
                PRIMARY KEY (Project_Id, Author_Id)
            )
        """)

    def create_project_lab_table(self):
        """
        Crée la table de liaison many-to-many entre les projets et les laboratoires.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Project_Lab (
                Project_Id INT,
                Lab_id INT,
                FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id) ON DELETE CASCADE,
                FOREIGN KEY (Lab_id) REFERENCES Lab(Lab_Id) ON DELETE CASCADE,
                PRIMARY KEY (Project_Id, Lab_id)
            )
        """)

    def create_project_forge_table(self):
        """
        Crée la table de liaison many-to-many entre les projets et les forges.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Project_Forge (
                Project_Id INT,
                Forge_id INT,
                FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id) ON DELETE CASCADE,
                FOREIGN KEY (Forge_id) REFERENCES Forge(Forge_Id) ON DELETE CASCADE,
                PRIMARY KEY (Project_Id, Forge_id)
            )
        """)

    def create_project_keyword_table(self):
        """
        Crée la table de liaison many-to-many entre les projets et les mots-clés.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Project_Keyword (
                Project_Id INT,
                Keyword_id INT,
                FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id) ON DELETE CASCADE,
                FOREIGN KEY (Keyword_id) REFERENCES Keyword(Keyword_Id) ON DELETE CASCADE,
                PRIMARY KEY (Project_Id, Keyword_id)
            )
        """)

    def create_project_language_table(self):
        """
        Crée la table de liaison many-to-many entre les projets et les languages.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Project_Language (
                Project_Id INT,
                Language_id INT,
                FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id) ON DELETE CASCADE,
                FOREIGN KEY (Language_id) REFERENCES Language(Language_Id) ON DELETE CASCADE,
                PRIMARY KEY (Project_Id, Language_id)
            )
        """)

    def create_project_source_table(self):
        """
        Crée la table de liaison many-to-many entre les projets et les sources.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Project_Source (
                Project_Id INT,
                Source_id INT,
                FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id) ON DELETE CASCADE,
                FOREIGN KEY (Source_id) REFERENCES Source(Source_Id) ON DELETE CASCADE,
                PRIMARY KEY (Project_Id, Source_id)
            )
        """)

    def create_project_github_table(self):
        """
        Crée la table de liaison entre Project et Github.
        
        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute('''CREATE TABLE Project_Github
                        (Project_Id INT,
                        Github_Id INT,
                        FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id),
                        FOREIGN KEY (Github_Id) REFERENCES Github(Github_Id),
                        PRIMARY KEY (Project_Id, Github_Id))''')

    def create_project_institution_table(self):
        """
        Crée la table de liaison many-to-many entre les projets et les institutions.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Project_Institution (
                Project_Id INT,
                Institution_Id INT,
                FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id) ON DELETE CASCADE,
                FOREIGN KEY (Institution_Id) REFERENCES Institution(Institution_Id) ON DELETE CASCADE,
                PRIMARY KEY (Project_Id, Institution_Id)
            )
        """)

    def insert_projects(self, projects, projects_github):
        """
        Insère les projets dans la table Project en évitant les doublons basés sur softCodeRepository.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
            projects (list): Liste des projets à insérer.
            projects_github (list): Liste des projets GitHub contenant les informations supplémentaires.
        """
        print("Inserting projects...")

        repository_set = set()  # Utilisé pour éviter les doublons de softCodeRepository
        for project in projects:

            soft_code_repository = project.get('softCodeRepository', '')

            # Ignorer les projets sans softCodeRepository ou déjà insérés
            if not soft_code_repository or soft_code_repository in repository_set:
                continue

            title = project.get('title', '')
            abstract = project.get('abstract', '')
            date_creation = project.get('submitted_date', '')
            date_update = project.get('updated_date', '')
            domain = project.get('domain', '')
            url = project.get('softCodeRepository')
            on_github = True

            # Extraire le nombre d'étoiles du projet GitHub correspondant
            github_info = next((item for item in projects_github if item['repo_url'] == soft_code_repository), None)

            # Mettre on_github à False si le projet n'est pas sur github
            if github_info is not None:
                stars = github_info.get('repo_info', {}).get('stars', "None")
            else:
                stars = "None" 
            
            if stars == "None":
                on_github = False

            # Requête SQL pour insérer les données
            insert_query = '''INSERT INTO Project 
                            (Title, Abstract, Date_creation, Date_update, Domain, Url, OnGithub) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            
            self.cursor.execute(insert_query, (title, abstract, date_creation, date_update, domain, url, on_github))

            # Récupérer l'ID du projet inséré pour les relations many-to-many
            project_id = self.cursor.lastrowid
            project['Project_Id'] = project_id

            # Ajouter le softCodeRepository à l'ensemble pour éviter les doublons
            repository_set.add(soft_code_repository)

        # Valider la transaction pour s'assurer que les données sont insérées
        self.conn.commit()



    def insert_authors(self, projects):
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
                author_mail = author_info.get('mail', '')
                author_hal_name_id = author_info.get('authIdHal_s', '')
                author_hal_number_id= author_info.get('authIdHal_i', '')
                author_github_id = author_info.get('AuthGithubId', '')
                if author_name not in author_set:  # Vérifie si l'auteur n'a pas déjà été inséré
                    self.cursor.execute("""
                        INSERT IGNORE INTO Author (Name, Mail, Hal_name_id, Hal_number_id, Github_Id) VALUES (%s, %s, %s, %s, %s)
                    """, (author_name.strip(), author_mail, author_hal_name_id.strip(), author_hal_number_id, author_github_id))
                    author_set.add(author_name)  # Ajoute l'auteur à l'ensemble pour éviter les doublons

    def insert_forges(self, projects):
        """
        Insère les forges dans la table Forge.

        Args:
            projects (list): Liste des projets contenant les informations sur les forges.
        """
        forge_set = set()  # Utilisé pour éviter les doublons
        for project in projects:
            url = project.get('softCodeRepository', '')
            if url:
                repo_site = url.split('//')[-1].split('/')[0]  # Extraire le nom de la forge
                if repo_site not in forge_set:
                    self.cursor.execute("""
                        INSERT IGNORE INTO Forge (Name) VALUES (%s)
                    """, (repo_site,))
                    forge_set.add(repo_site)  # Ajoute la forge à l'ensemble pour éviter les doublons


    def insert_labs(self, projects):
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
                self.cursor.execute("""
                    INSERT IGNORE INTO Lab (Name) VALUES (%s)
                """, (laboratory,))
                lab_set.add(laboratory)  # Ajoute le laboratoire à l'ensemble pour éviter les doublons

    def insert_keywords(self, projects):
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
                    self.cursor.execute("""
                        INSERT IGNORE INTO Keyword (Label) VALUES (%s)
                    """, (keyword,))
                    keyword_set.add(keyword)  # Ajoute le mot-clé à l'ensemble pour éviter les doublons

    def insert_institutions(self, projects):
        """
        Insère les institutions dans la table Institution.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
            projects (list): Liste des projets contenant les informations sur les institutions.
        """
        institution_set = set()  # Utilisé pour éviter les doublons
        for project in projects:
            institutions = project.get('institution', '').split(',')
            for institution in institutions:
                institution = institution.strip()
                if institution and institution not in institution_set:
                    self.cursor.execute("""
                        INSERT IGNORE INTO Institution (Name) VALUES (%s)
                    """, (institution,))
                    institution_set.add(institution)  # Ajoute l'institution à l'ensemble pour éviter les doublons

    def insert_languages(self, projects):
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
                    self.cursor.execute("""
                        INSERT IGNORE INTO Language (Name) VALUES (%s)
                    """, (language,))
                    language_set.add(language)  # Ajoute le language à l'ensemble pour éviter les doublons

    def insert_sources(self, projects):
        """
        Insère les sources dans la table Source.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
            projects (list): Liste des projets contenant les informations sur les sources.
        """
        source_set = set()  # Utilisé pour éviter les doublons
        for project in projects:
            source = project.get('source', '')
            hal_id = project.get('hal_id', '')
            github_id = project.get('github_id', '')
            sh_id = project.get('sh_id', '')

            # Créer une clé unique pour éviter les doublons
            source_key = (source, hal_id, github_id)
            
            if source_key not in source_set:
                self.cursor.execute("""
                    INSERT IGNORE INTO Source (Name, Hal_id, Github_id, Sh_id) VALUES (%s, %s, %s, %s)
                """, (source, hal_id, github_id, sh_id))
                source_set.add(source_key)  # Ajoute la clé à l'ensemble pour éviter les doublons

    def insert_github(self, projects):
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
                            (Name, Full_Name, Description, Stars, Forks, Owner, Subscribers, Open_Issues, 
                            Contributors_Url, Pulls_Url, Commits_Url, Releases_Url, Language, 
                            Created_At, Updated_At, Pushed_At, Homepage, Repo_Url) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            self.cursor.execute(insert_query, (
                repo_info.get('name'),
                repo_info.get('full_name'),
                repo_info.get('description'),
                repo_info.get('stars'),
                repo_info.get('forks'),
                repo_info.get('owner'),
                repo_info.get('subscribers'),
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
    def insert_project_authors(self, projects):
        """
        Insère la relation many-to-many entre les projets et les auteurs dans la table de liaison Project_Author.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
            projects (list): Liste des projets contenant les informations sur les auteurs.
        """
        for project in projects:
            
            self.cursor.execute("""
                SELECT Project_Id FROM Project WHERE url = %s
            """, (project.get('softCodeRepository', ''),))
            project_result = self.cursor.fetchone()
            self.cursor.fetchall()
            if project_result is None:
                continue
            Project_Id = project_result[0]

            authors = project.get('authors', [])
            for author_info in authors:
                author_name = author_info.get('name', '')
                
                # Récupérer l'ID de l'auteur depuis la table Author
                self.cursor.execute("""
                    SELECT Author_Id FROM Author WHERE Name = %s
                """, (author_name.strip(),))
                author_result = self.cursor.fetchone()
                self.cursor.fetchall()
                if author_result is None:
                    continue

                Author_Id = author_result[0]

                # Insérer la relation many-to-many dans la table de liaison
                self.cursor.execute("""
                    INSERT IGNORE INTO Project_Author (Project_Id, Author_Id) VALUES (%s, %s)
                """, (Project_Id, Author_Id))

    def insert_project_labs(self, projects):
        """
        Insère la relation many-to-many entre les projets et les laboratoires dans la table de liaison Project_Lab.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
            projects (list): Liste des projets contenant les informations sur les laboratoires.
        """
        for project in projects:
            # Récupérer l'ID du projet depuis la table Project
            self.cursor.execute("""
                SELECT Project_Id FROM Project WHERE url = %s
            """, (project.get('softCodeRepository', ''),))
            project_result = self.cursor.fetchone()
            self.cursor.fetchall()
            if project_result is None:
                continue
            Project_Id = project_result[0]

            # Récupérer le laboratoire associé au projet
            lab_name = project.get('laboratory', '').strip()
            if lab_name:
                # Récupérer l'ID du laboratoire depuis la table Lab
                self.cursor.execute("""
                    SELECT Lab_Id FROM Lab WHERE Name = %s
                """, (lab_name,))
                lab_result = self.cursor.fetchone()
                self.cursor.fetchall()
                if lab_result is None:
                    continue

                lab_id = lab_result[0]

                # Insérer la relation many-to-many dans la table de liaison
                self.cursor.execute("""
                    INSERT IGNORE INTO Project_Lab (Project_Id, Lab_id) VALUES (%s, %s)
                """, (Project_Id, lab_id))

    def insert_project_forges(self, projects):
        """
        Insère la relation many-to-many entre les projets et les forges dans la table de liaison Project_Forge.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
            projects (list): Liste des projets contenant les informations sur les forges.
        """
        for project in projects:
            # Récupérer l'ID du projet depuis la table Project
            self.cursor.execute("""
                SELECT Project_Id FROM Project WHERE url = %s
            """, (project.get('softCodeRepository', ''),))
            project_result = self.cursor.fetchone()
            self.cursor.fetchall()
            if project_result is None:
                continue
            Project_Id = project_result[0]

            # Récupérer l'URL du dépôt de code associé au projet
            url = project.get('softCodeRepository', '').strip()
            if url:
                repo_site = url.split('//')[-1].split('/')[0]  # Extraire le nom de la forge

                # Récupérer l'ID de la forge depuis la table Forge
                self.cursor.execute("""
                    SELECT Forge_Id FROM Forge WHERE Name = %s
                """, (repo_site,))
                forge_result = self.cursor.fetchone()
                self.cursor.fetchall()
                if forge_result is None:
                    continue
                forge_id = forge_result[0]

                # Insérer la relation many-to-many dans la table de liaison
                self.cursor.execute("""
                    INSERT IGNORE INTO Project_Forge (Project_Id, Forge_id) VALUES (%s, %s)
                """, (Project_Id, forge_id))


    def insert_project_keywords(self, projects):
        """
        Insère la relation many-to-many entre les projets et les mots-clés dans la table de liaison Project_Keyword.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
            projects (list): Liste des projets contenant les informations sur les mots-clés.
        """
        for project in projects:
            # Récupérer l'ID du projet depuis la table Project
            self.cursor.execute("""
                SELECT Project_Id FROM Project WHERE url = %s
            """, (project.get('softCodeRepository', ''),))
            project_result = self.cursor.fetchone()
            self.cursor.fetchall()
            if project_result is None:
                continue
            Project_Id = project_result[0]

            # Récupérer les mots-clés associés au projet
            keywords = project.get('keywords', '').split(',')
            for keyword in keywords:
                keyword = keyword.strip()
                if keyword:
                    # Récupérer l'ID du mot-clé depuis la table Keyword
                    self.cursor.execute("""
                        SELECT Keyword_Id FROM Keyword WHERE Label = %s
                    """, (keyword,))
                    keyword_result = self.cursor.fetchone()
                    self.cursor.fetchall()
                    if keyword_result is None:
                        continue
                    keyword_id = keyword_result[0]

                    # Insérer la relation many-to-many dans la table de liaison
                    self.cursor.execute("""
                        INSERT IGNORE INTO Project_Keyword (Project_Id, Keyword_id) VALUES (%s, %s)
                    """, (Project_Id, keyword_id))

    def insert_project_languages(self, projects):
        """
        Insère la relation many-to-many entre les projets et les languages dans la table de liaison Project_Language.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
            projects (list): Liste des projets contenant les informations sur les languages.
        """
        for project in projects:
            # Récupérer l'ID du projet depuis la table Project
            self.cursor.execute("""
                SELECT Project_Id FROM Project WHERE url = %s
            """, (project.get('softCodeRepository', ''),))
            project_result = self.cursor.fetchone()
            self.cursor.fetchall()
            if project_result is None:
                continue
            Project_Id = project_result[0]

            languages = project.get('softProgrammingLanguage', [])
            for language in languages:
                language = language.strip()
                
                # Récupérer l'ID du language depuis la table Language
                self.cursor.execute("""
                    SELECT Language_Id FROM Language WHERE Name = %s
                """, (language,))
                language_result = self.cursor.fetchone()
                self.cursor.fetchall()
                if language_result is None:
                    continue

                language_id = language_result[0]

                # Insérer la relation many-to-many dans la table de liaison
                self.cursor.execute("""
                    INSERT IGNORE INTO Project_Language (Project_Id, Language_id) VALUES (%s, %s)
                """, (Project_Id, language_id))

    def insert_project_sources(self, projects):
        """
        Insère la relation many-to-many entre les projets et les sources dans la table de liaison Project_Source.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
            projects (list): Liste des projets contenant les informations sur les sources.
        """
        for project in projects:
            # Récupérer l'ID du projet depuis la table Project
            self.cursor.execute("""
                SELECT Project_Id FROM Project WHERE Url = %s
            """, (project.get('softCodeRepository', ''),))
            project_result = self.cursor.fetchone()
            self.cursor.fetchall()
            if project_result is None:
                continue
            Project_Id = project_result[0]

            source = project.get('source', '').strip()
            if source:
                # Récupérer l'ID de la source depuis la table Source
                self.cursor.execute("""
                    SELECT Source_Id FROM Source WHERE Name = %s
                """, (source,))
                source_result = self.cursor.fetchone()
                self.cursor.fetchall()
                if source_result is None:
                    continue
                source_id = source_result[0]

                # Insérer la relation many-to-many dans la table de liaison
                self.cursor.execute("""
                    INSERT IGNORE INTO Project_Source (Project_Id, Source_id) VALUES (%s, %s)
                """, (Project_Id, source_id))

    def insert_project_github_relations(self, projects, projects_github):
        """
        Insère les relations entre les projets et leurs informations GitHub dans la table de liaison.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
            projects (list): Liste des projets contenant les relations à insérer.
            projects_github (list): Liste des projets GitHub contenant les informations supplémentaires.
        """
        for project in projects:
            url = project.get('softCodeRepository')

            # Récupérer l'ID du projet depuis la table Project
            self.cursor.execute("SELECT Project_Id FROM Project WHERE Url = %s", (url,))
            project_result = self.cursor.fetchone()
            self.cursor.fetchall()
            if not project_result:
                #print(f"Projet '{title}' non trouvé dans la table Project.")
                continue
            project_id = project_result[0]

            # Récupérer l'ID du projet GitHub depuis la table Github
            github_info = next((item for item in projects_github if item['repo_url'] == url), None)
            if not github_info or 'repo_info' not in github_info:
                #print(f"Projet GitHub pour '{title}' non trouvé ou sans informations dans les projets GitHub.")
                continue
            
            # Récupérer l'ID du dépôt GitHub depuis la table Github
            self.cursor.execute("SELECT Github_Id FROM Github WHERE Full_Name = %s", (github_info['repo_info']['full_name'],))
            github_result = self.cursor.fetchone()
            self.cursor.fetchall()
            if not github_result:
                #print(f"Dépôt GitHub '{github_info['repo_info']['full_name']}' non trouvé dans la table Github.")
                continue
            github_id = github_result[0]

            # Insérer la relation dans la table de liaison Project_Github
            insert_query = '''INSERT IGNORE INTO Project_Github (Project_Id, Github_Id) VALUES (%s, %s)'''
            self.cursor.execute(insert_query, (project_id, github_id))

    def insert_project_institutions(self, projects):
        """
        Insère la relation many-to-many entre les projets et les institutions dans la table de liaison Project_Institution.

        Args:
            cursor: Curseur MySQL pour exécuter les requêtes SQL.
            projects (list): Liste des projets contenant les informations sur les institutions.
        """
        for project in projects:
            # Récupérer l'ID du projet depuis la table Project
            self.cursor.execute("""
                SELECT Project_Id FROM Project WHERE url = %s
            """, (project.get('softCodeRepository', ''),))
            project_result = self.cursor.fetchone()
            self.cursor.fetchall()
            if project_result is None:
                continue
            Project_Id = project_result[0]

            # Récupérer l'ID de l'institution depuis la table Institution
            self.cursor.execute("""
                SELECT Institution_Id FROM Institution WHERE Name = %s
            """, (project.get('institution', ''),))
            institution_result = self.cursor.fetchone()
            self.cursor.fetchall()
            if institution_result is None:
                continue
            institution_id = institution_result[0]

            # Insérer la relation many-to-many dans la table de liaison
            self.cursor.execute("""
                INSERT IGNORE INTO Project_Institution (Project_Id, Institution_Id) VALUES (%s, %s)
            """, (Project_Id, institution_id))

    def create_database(self, db_name):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        self.cursor.execute(f"USE {db_name}")

    def drop_database_if_exists(self, db_name):
        self.cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")

    def fill_database(self, projects, projects_github):

        self.create_project_table()
        self.insert_projects(projects, projects_github)

        self.create_author_table()
        self.insert_authors(projects)

        self.create_forge_table()
        self.insert_forges(projects)

        self.create_lab_table()
        self.insert_labs(projects)

        self.create_keyword_table()
        self.insert_keywords(projects)

        self.create_institution_table()
        self.insert_institutions(projects)

        self.create_language_table()
        self.insert_languages(projects)

        self.create_source_table()
        self.insert_sources(projects)

        self.create_github_table()
        self.insert_github(projects_github)

        self.create_project_author_table()
        self.insert_project_authors(projects)

        self.create_project_lab_table() 
        self.insert_project_labs(projects)

        self.create_project_forge_table()
        self.insert_project_forges(projects)

        self.create_project_keyword_table()
        self.insert_project_keywords(projects)

        self.create_project_language_table()
        self.insert_project_languages(projects)

        self.create_project_source_table()
        self.insert_project_sources(projects)

        self.create_project_github_table()
        self.insert_project_github_relations(projects, projects_github)

        self.create_project_institution_table()
        self.insert_project_institutions(projects)

        self.conn.commit()
        
        print("Données insérées avec succès dans la base de données.")

    def complete_database(self, projects, projects_github):
        self.insert_projects(projects, projects_github)
        self.insert_authors(projects)
        self.insert_forges(projects)
        self.insert_labs(projects)
        self.insert_keywords(projects)
        self.insert_institutions(projects)
        self.insert_languages(projects)
        self.insert_sources(projects)
        self.insert_github(projects_github)
        self.insert_project_authors(projects)
        self.insert_project_labs(projects)
        self.insert_project_forges(projects)
        self.insert_project_keywords(projects)
        self.insert_project_languages(projects)
        self.insert_project_sources(projects)
        self.insert_project_github_relations(projects, projects_github)
        self.insert_project_institutions(projects)
        self.conn.commit()

        print("Données rajoutées avec succès dans la base de données.")

def main():
    json_file_hal = 'CNRS_HAL_GITMOD1.json' 
    json_file_github = 'CNRS_HAL_GITHUB_GITMOD1.json'
    db_config = {
        'host': 'localhost',
        'user': 'mouahid',
        'password': 'MdpSQL',
        'database': 'cnrs_hal_db'
    }

    db_manager = DatabaseManager(db_config)
    data_hal = db_manager.load_json_data(json_file_hal)
    projects = data_hal.get('projects', [])

    data_github = db_manager.load_json_data(json_file_github)
    projects_github = data_github.get('projects', [])

    db_manager.connect()
    db_manager.drop_database_if_exists(db_config['database'])
    db_manager.create_database(db_config['database'])
    db_manager.fill_database(projects, projects_github)
    db_manager.close()

if __name__ == '__main__':
    main()
