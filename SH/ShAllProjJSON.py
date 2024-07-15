import requests
import time
import json
from urllib.parse import urljoin

def fetch_all_data(token):
    state_file = "fetch_state.json"  # Nom du fichier d'état
    base_url = "https://archive.softwareheritage.org/api/1/origin/search/cnrs/"
    headers = {"Authorization": f"Bearer {token}"}
    all_data = []
    params = {'per_page': 2}

    # Vérifier si le fichier d'état existe et charger l'état
    try:
        with open(state_file, "r") as file:
            state = json.load(file)
            base_url = state["next_url"]  # URL de la prochaine page à traiter
            all_data = state["data"]  # Données déjà récupérées
    except FileNotFoundError:
        print("Aucun fichier d'état trouvé, démarrage d'une nouvelle récupération.")

    def get_next_page_link(headers):
        link_header = headers.get('Link', '')
        links = [link.split(';') for link in link_header.split(',')]
        next_link = [link for link in links if len(link) > 1 and 'rel="next"' in link[1]]
        if next_link:
            return next_link[0][0].strip('<> ')
        return None

    def handle_rate_limiting(headers):
        remaining = int(headers.get('X-RateLimit-Remaining', 0))
        reset_time = int(headers.get('X-RateLimit-Reset', 0))
        if remaining == 0:
            sleep_time = reset_time - int(time.time()) + 1
            if sleep_time > 0:
                print(f"Rate limit reached. Sleeping for {sleep_time} seconds.")
                time.sleep(sleep_time)

    while True:
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            all_data.extend(data)
            handle_rate_limiting(response.headers)
            next_page_url = get_next_page_link(response.headers)
            if not next_page_url:
                break
            base_url = urljoin(base_url, next_page_url)
            params = {}

            # Sauvegarder l'état après chaque page traitée
            with open(state_file, "w") as file:
                json.dump({"next_url": base_url, "data": all_data}, file)

        except requests.exceptions.HTTPError as e:
            print(f"Erreur HTTP: {e}")
            if e.response.status_code == 429:
                print("Limite de taux atteinte, attente de 60 secondes avant de réessayer...")
                time.sleep(60)
                continue
            else:
                break

    return all_data

# Transforme les données en un format structuré avec les clés appropriées
def structure_data(data):
    structured_data = {"number_of_projects": len(data), "projects": []}
    for i, item in enumerate(data, start=1):
        project_info = {
            "project_number": i,
            "url": item.get('url', 'N/A'),
            "visit_types": item.get('visit_types', []),
            "has_visits": item.get('has_visits', False),
            "origin_visits_url": item.get('origin_visits_url', 'N/A'),
            "metadata_authorities_url": item.get('metadata_authorities_url', 'N/A'),
        }
        structured_data["projects"].append(project_info)
    return structured_data

# Utilisez votre token ici
token = "YOUR_PERSONAL_SH_TOKEN"
data = fetch_all_data(token)
structured_data = structure_data(data)

# Enregistrer les données structurées dans un fichier JSON
output_file = "structured_data_cnrs.json"
with open(output_file, "w") as file:
    json.dump(structured_data, file, indent=2)

print(f"Données structurées enregistrées dans {output_file}")
