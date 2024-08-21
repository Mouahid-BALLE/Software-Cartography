# importer la classe DatabaseManager depuis le fichier database_manager.py
from DataBase import DatabaseManager

""" Complete la base de données avec les nouvelles données enregistrées dans un fichier JSON. """

def main():
    # Configuration de la base de données
    db_config = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'cnrs_db'
    }
    
    # Chemins vers les nouveaux fichiers JSON
    new_json_file_ext = '../Ext/ExtJSON.json'
    new_json_file_sh = '../SH/SH_CNRS_PROJ_INFO.json'
    new_json_file_owner_sh = '../Github/CNRS_GITHUB_SH_OWNERS_REPOS.json'
    new_json_file_gitlab= '../GitLab/transformed_projects.json'
    new_json_file_github = '../GitHUB/CNRS_GITHUB_FROM_HAL.json'
    
    # Créer une instance de DatabaseManager
    db_manager = DatabaseManager(db_config)
    
    # Charger les nouvelles données JSON
    new_data_hal = db_manager.load_json_data(new_json_file_owner_sh)
    new_projects = new_data_hal.get('projects', [])

    # Connexion à la base de données
    db_manager.connect()
    
    # Insérer les nouvelles données dans la base de données
    db_manager.complete_database(new_projects)
    
    # Fermer la connexion à la base de données
    db_manager.close()
    
    print("Nouvelles données insérées avec succès dans la base de données.")

if __name__ == '__main__':
    main()
