import json

# Description : Ce script concatène plusieurs fichiers JSON contenant des données de projets
# en un seul fichier JSON. Il lit les données de chaque fichier JSON spécifié dans une liste,
# les combine dans une seule liste, puis sauvegarde cette liste combinée dans un nouveau fichier JSON.

# Entrées :
# - `file_list` : Liste des chemins de fichiers JSON à concaténer.
#
# Sorties :
# - `output_file` : Fichier JSON contenant toutes les données de projets concaténées.

def concat_json_files(file_list, output_file):
    """
    Concatène plusieurs fichiers JSON en un seul.

    Args:
        file_list (list): Liste des chemins des fichiers JSON à concaténer.
        output_file (str): Chemin du fichier JSON de sortie.

    Returns:
        None
    """
    all_labs_data = []

    # Lire tous les fichiers JSON spécifiés
    for file_path in file_list:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for lab_data in data:
                all_labs_data.append(lab_data)

    # Sauvegarder les projets concaténés dans un fichier JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_labs_data, f, ensure_ascii=False, indent=4)

    print(f"Toutes les informations des projets ont été sauvegardées dans '{output_file}'.")

if __name__ == "__main__":
    # Liste des fichiers JSON à concaténer
    file_list = [
        'LAB_RESERVED_GITLAB.json', 
        'LAB_ON_OTHER_GITLAB.json', 
        'LAB_ON_SHARED_GITLAB.json' 
    ]
    output_file = 'concatenated_projects.json'  # Nom du fichier de sortie
    concat_json_files(file_list, output_file)
