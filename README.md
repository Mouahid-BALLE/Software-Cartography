# Cartographie des Logiciels Open Source du CNRS

Ce projet vise à construire une cartographie des logiciels open sources issus du CNRS, ou des logiciels auxquels des chercheurs du CNRS contribuent. Les sources d'information utilisées sont GitHub, Software Heritage et HAL. Cette cartographie met en évidence :

- L’ensemble des logiciels concernés
- Une répartition par unité de recherche
- Les logiciels les plus visibles (nombre de « stars » par exemple)
- Les thématiques les plus représentées

## Prérequis
- Python 3.x
- [MySQL](https://dev.mysql.com/downloads/installer/)

## Packages et Bibliothèques

Les bibliothèques Python suivantes sont nécessaires pour exécuter ce script :

- mysql-connector-python
- requests
- re
- json

Pour installer les packages nécessaires, utilisez [pip](https://pip.pypa.io/en/stable/) :

```bash
pip install mysql-connector-python requests
```

## Installation

Clonez ce dépôt sur votre machine locale :

```bash
git clone <URL_du_depot>
cd <nom_du_depot>
```


## Configuration

Créez un fichier JSON pour les données de HAL (par exemple, CNRS_HAL.json) et un autre pour les données GitHub (par exemple, CNRS_GITHUB.json).

Configurez les informations de connexion à la base de données MySQL dans la section db_config du script.

## Utilisation

**Récupération des données HAL**

Créez un fichier JSON pour stocker les données HAL.

Exécutez le script 
```bash
python HalJSON.py
```
**Récupération des données GitHub**

Créez une instance de GitHalJSON avec votre token GitHub personnel.
Mon token disponible dans le code ne fonctionne plus il faut le remplacer par le votre( voir section token d'acces plus bas).

Exécutez le script python GitHalJSON.py :

```bash
python GitHalJSON.py
```
Assurez-vous que ces fichiers JSON suivent la structure attendue par le script. Exemple de structure pour CNRS_GITHUB.json :
```json
{
    "projects": [
        {
            "project_number": 3,
            "title": "Marcelle",
            "repo_source": "softCodeRepository",
            "repo_url": "https://github.com/marcellejs/marcelle/",
            "repo_info": {
                "name": "marcelle",
                "full_name": "marcellejs/marcelle",
                "description": "An Interactive Machine Learning Toolkit",
                "stars": 43,
                "forks": 7,
                "owner": "marcellejs",
                "watchers": 43,
                "open_issues": 5,
                "contributors_url": "https://api.github.com/repos/marcellejs/marcelle/contributors",
                "pulls_url": "https://api.github.com/repos/marcellejs/marcelle/pulls{/number}",
                "commits_url": "https://api.github.com/repos/marcellejs/marcelle/commits{/sha}",
                "releases_url": "https://api.github.com/repos/marcellejs/marcelle/releases{/id}",
                "language": "TypeScript",
                "created_at": "2020-06-26T13:37:00Z",
                "updated_at": "2024-05-15T09:03:05Z",
                "pushed_at": "2024-06-14T20:21:31Z",
                "homepage": "https://marcelle.dev",
                "repo_url": "https://github.com/marcellejs/marcelle"
            }
        }
    ]
}
```

**Création et Remplissage de la Base de Données**

Configurez les informations de connexion à la base de données MySQL dans la section db_config du script HalDB.py :
```bash
db_config = {
     'host': 'localhost',
     'user': 'mouahid',
     'password': 'MonMdp',
     'database': 'cnrs_hal_db'
}
```
Exécutez le script principal pour créer et remplir la base de données :

```bash
python HalDB.py
```

**Tokens d'accès**

Pour accéder aux données des API GitHub, vous pouvez avoir besoin de tokens d'accès pour respecter les limites de taux et garantir un accès continu. Vous pouvez le récupérer directement sur [Github](https://github.com/settings/tokens) et configurer les tokens d'accès dans les appels d'API au besoin.



## Affichage des Informations

Par exemple pour afficher les informations de tous les projets qui sont sur  GitHub, utilisez la requête SQL suivante :

```sql
SELECT Project.*, Github.*
FROM Project
JOIN Project_Github ON Project.Project_Id = Project_Github.Project_Id
JOIN Github ON Project_Github.Github_Id = Github.Github_Id;
```

Cette requête effectue une jointure entre les tables Project, Project_Github et Github pour récupérer toutes les informations des projets présents sur GitHub.
