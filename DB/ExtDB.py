# importer la classe DatabaseManager depuis le fichier database_manager.py
from DataBase import DatabaseManager

""" Complete la base de données avec les nouvelles données JSON. """

def main():
    # Configuration de la base de données
    db_config = {
        'host': 'localhost',
        'user': 'mouahid',
        'password': 'MdpSQL',
        'database': 'cnrs_hal_db'
    }
    
    # Chemins vers les nouveaux fichiers JSON
    #new_json_file = '../Ext/ExtJSON.json'
    new_json_file = '../SH/SH_CNRS_PROJ_INFO.json'
    new_json_file_github = '../GitHUB/CNRS_GITHUB_FROM_HAL.json'
    
    # Créer une instance de DatabaseManager
    db_manager = DatabaseManager(db_config)
    
    # Charger les nouvelles données JSON
    new_data_hal = db_manager.load_json_data(new_json_file)
    new_projects = new_data_hal.get('projects', [])

    new_data_github = db_manager.load_json_data(new_json_file_github)
    new_projects_github = new_data_github.get('projects', [])

    # Connexion à la base de données
    db_manager.connect()
    
    # Insérer les nouvelles données dans la base de données
    db_manager.complete_database(new_projects, new_projects_github)
    
    # Fermer la connexion à la base de données
    db_manager.close()
    
    print("Nouvelles données insérées avec succès dans la base de données.")

if __name__ == '__main__':
    main()
