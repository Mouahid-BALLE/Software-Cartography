# CNRS Software Cartography

## Description

Ce projet vise à créer une cartographie des logiciels open source développés ou soutenus par le CNRS. Il s'appuie sur des données collectées à partir des API de GitHub, GitLab, Software Heritage, et HAL pour analyser et visualiser les contributions des chercheurs du CNRS.

## Structure du Projet

Le projet est organisé en plusieurs dossiers, chacun dédié à une tâche spécifique :

### 1. `hal/`
Le dossier `hal/` est dédié à la collecte des projets CNRS présents sur la plateforme **HAL (Hyper Article en Ligne)**. Les scripts permettent d'extraire les informations des projets, de les organiser en catégories, et de les sauvegarder sous forme de fichiers JSON.

### 2. `sh/`
Ce dossier contient les scripts utilisés pour collecter les informations des projets depuis la forge **Software Heritage (SH)**. Les données des projets sont récupérées et structurées dans des fichiers JSON pour une analyse ultérieure.

### 3. `gitlab/`
Le dossier `gitlab/` contient des scripts qui permettent de collecter les informations des projets hébergés sur **GitLab**, ainsi que les contenus des fichiers README associés. Les données sont ensuite enregistrées dans des fichiers JSON.

### 4. `github/`
Ce dossier est similaire à celui de GitLab, mais pour la plateforme **GitHub**. Les scripts récupèrent les informations des projets GitHub, extraient les contenus des fichiers README, et les sauvegardent dans des fichiers JSON.

### 5. `ext/`
Le dossier `ext/` est utilisé pour collecter les informations des projets externes provenant de sources non répertoriées dans les autres dossiers. Le script lit des fichiers texte contenant les URLs des projets et génère des fichiers JSON structurés.

### 6. `readme/`
Le dossier `readme/` contient des scripts dédiés à l'extraction et à l'analyse des fichiers README et des abstracts des projets afin d'obtenir leur domaine scientifique.

### 7. `db/`
Ce dossier contient des scripts qui interagissent directement avec une base de données MySQL. Ils permettent de centraliser les données collectées depuis différentes sources (GitHub, GitLab, SH, HAL, etc.), de les fusionner dans une base de données, puis de les exporter pour une analyse plus approfondie. Ce dossier inclut également des scripts pour générer des graphiques et des fichiers CSV à partir des données stockées.

## Prérequis

- Python 3.x
- MySQL pour la gestion de la base de données
- Bibliothèques Python nécessaires (voir `requirements.txt`)
- Accès à des clés API pour GitHub et Software Heritage

## Installation

1. Clonez ce dépôt :

    ```bash
    git clone https://github.com/Mouahid-BALLE/Software-Cartography
    cd Software-Cartography
    ```

2. Installez les dépendances Python :

    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

1. **Configuration** :
    - Mettez à jour les fichiers de configuration avec vos clés API et vos informations MySQL.

2. **Collecte des Données** :
    - Exécutez les scripts présents dans les dossiers `hal/`, `sh/`, `gitlab/`, `github/`, et `ext/` pour collecter les données depuis les différentes sources.
    - Les scripts se connectent aux APIs des forges, récupèrent les informations des projets, et les sauvegardent sous forme de fichiers JSON.

3. **Fusion des Données** :
    - Utilisez les scripts du dossier `db/` pour centraliser et fusionner les données collectées dans une base de données MySQL.
    - Les scripts permettent également d'exporter ces données sous forme de fichiers CSV ou de générer des rapports graphiques pour une analyse plus approfondie.

## Remerciements

Merci à Monsieur SCUTURICI Vasile-Marian pour son soutien et son aide précieuse tout au long du développement de ce projet.
