import json

"""
Description : Ce script fusionne plusieurs fichiers JSON contenant des README, 
en un seul fichier JSON consolidé. Il parcourt chaque fichier JSON spécifié, 
concatène les données qu'ils contiennent, et enregistre le résultat dans un 
fichier de sortie unique.

Entrées :
- `json_files` : Liste des chemins vers les fichiers JSON à concaténer. Chaque fichier contient des données sous forme de liste.
  
Sorties :
- `output_file` : Fichier JSON où seront sauvegardées les données concaténées de tous les fichiers JSON en entrée.
"""


def concat_json_files(json_files, output_file):
    # Liste pour stocker les données concaténées
    concatenated_data = []

    # Parcourir tous les fichiers JSON dans la liste spécifiée
    for filepath in json_files:
        try:
            # Ouvrir et lire le contenu du fichier JSON
            with open(filepath, 'r', encoding='utf-8') as file:
                # Charger les données du fichier JSON
                data = json.load(file)
                # Ajouter les données au tableau principal
                concatenated_data.extend(data)
        except json.JSONDecodeError:
            print(f"Erreur lors du décodage de {filepath}. Le fichier sera ignoré.")
        except FileNotFoundError:
            print(f"Fichier non trouvé: {filepath}. Il sera ignoré.")

    # Sauvegarder les données concaténées dans un fichier de sortie
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Écrire les données sous forme JSON avec une indentation de 4 espaces pour la lisibilité
        json.dump(concatenated_data, outfile, indent=4)

# Exemple d'utilisation
json_gitlab_readme_files = [
    'CNRS_GITLAB_README.json',
    '../Github/README_HAL.json',
    '../Github/README_SH.json' 
]

output_file = 'CNRS_README.json'
concat_json_files(json_gitlab_readme_files, output_file)
