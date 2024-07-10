import json
import os

class JsonMerger:
    def __init__(self, output_file='merged_data.json'):
        """
        Initialise la classe avec le fichier de sortie.

        Args:
            output_file (str): Le chemin vers le fichier JSON de sortie.
        """
        self.output_file = output_file
        self.merged_data = []

    def load_json_data(self, json_file):
        """
        Charge les données d'un fichier JSON.

        Args:
            json_file (str): Le chemin vers le fichier JSON.

        Returns:
            dict: Les données JSON.
        """
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def merge_files(self, json_files):
        """
        Merge plusieurs fichiers JSON en une seule structure.

        Args:
            json_files (list): Liste des chemins vers les fichiers JSON à fusionner.
        """
        for file in json_files:
            data = self.load_json_data(file)
            self.merged_data.extend(data["projects"])

    def save_merged_data(self):
        """
        Sauvegarde les données fusionnées dans un fichier JSON.
        """
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump({"projects": self.merged_data}, f, ensure_ascii=False, indent=4)

    def merge_and_save(self, json_files):
        """
        Fusionne plusieurs fichiers JSON et enregistre le résultat.

        Args:
            json_files (list): Liste des chemins vers les fichiers JSON à fusionner.
        """
        self.merge_files(json_files)
        self.save_merged_data()
        print(f"Données fusionnées enregistrées dans {self.output_file}")

# utilisation
if __name__ == "__main__":
    json_files = ['CNRS_HAL.json', '../Git/CNRS_GITHUB_OWNERS_REPOS.json'] 
    merger = JsonMerger(output_file='CNRS_HAL_GITMOD1.json')
    merger.merge_and_save(json_files)

    json_github_files = ['../Git/CNRS_GITHUB.json', '../Git/CNRS_OWNERS_REPO_INFO.json'] 
    merger = JsonMerger(output_file='CNRS_HAL_GITHUB_GITMOD1.json')
    merger.merge_and_save(json_github_files)