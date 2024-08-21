import json
import os

"""
Description : Ce script fusionne plusieurs fichiers JSON contenant des informations sur des projets de recherche en un seul fichier JSON consolidé. 
Chaque fichier JSON en entrée contient des données structurées sur des projets provenant de différentes sources (HAL, GitHub, GitLab, etc.). 
Le script lit chaque fichier JSON, fusionne les données sous une structure unifiée, et enregistre le résultat dans un fichier JSON de sortie.

Entrées :
- `json_files` : Liste des chemins vers les fichiers JSON à fusionner. Chaque fichier contient des informations sur les projets structurées sous la clé "projects".

Sorties :
- `output_file` : Fichier JSON où seront sauvegardées les données fusionnées de tous les fichiers JSON en entrée.
"""


class JsonMerger:
    def __init__(self, output_file='merged_data.json'):
        """
        Initialise la classe avec le fichier de sortie.

        Args:
            output_file (str): Le chemin vers le fichier JSON de sortie.
        """
        self.output_file = output_file
        self.merged_data = []
        print(f"Initialisation: fichier de sortie = {self.output_file}")

    def load_json_data(self, json_file):
        """
        Charge les données d'un fichier JSON.

        Args:
            json_file (str): Le chemin vers le fichier JSON.

        Returns:
            dict: Les données JSON.
        """
        print(f"Chargement des données depuis {json_file}")
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def merge_files(self, json_files):
        """
        Merge plusieurs fichiers JSON en une seule structure.

        Args:
            json_files (list): Liste des chemins vers les fichiers JSON à fusionner.
        """
        print("Début de la fusion des fichiers")
        for file in json_files:
            print(f"Fusion du fichier {file}")
            try:
                data = self.load_json_data(file)
                self.merged_data.extend(data["projects"])
                print(f"Fichier {file} fusionné avec succès")
            except Exception as e:
                print(f"Erreur lors de la fusion du fichier {file}: {e}")

    def save_merged_data(self):
        """
        Sauvegarde les données fusionnées dans un fichier JSON.
        """
        print(f"Sauvegarde des données fusionnées dans {self.output_file}")
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump({"projects": self.merged_data}, f, ensure_ascii=False, indent=4)
        print("Données fusionnées sauvegardées avec succès")

    def merge_and_save(self, json_files):
        """
        Fusionne plusieurs fichiers JSON et enregistre le résultat.

        Args:
            json_files (list): Liste des chemins vers les fichiers JSON à fusionner.
        """
        print("Début du processus de fusion et de sauvegarde")
        self.merge_files(json_files)
        self.save_merged_data()
        print(f"Données fusionnées enregistrées dans {self.output_file}")

# utilisation
if __name__ == "__main__":
    json_files = [
        '../hal/CNRS_HAL.json', 
        '../Github/CNRS_GITHUB_HAL_COMPLET.json', 
        '../SH/SH_CNRS_PROJ_INFO.json', 
        '../Github/CNRS_GITHUB_SH_COMPLET.json', 
        '../Gitlab/CNRS_GITLAB.json', 
        '../Ext/ExtJSON.json'
    ]


    merger = JsonMerger(output_file='CNRS_REPOS.json')
    merger.merge_and_save(json_files)

