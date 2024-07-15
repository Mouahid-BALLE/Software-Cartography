import requests
import logging
import json
import os
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get the latest visit information of a repository
def get_last_visit_info(origin_url, headers):
    """
    Get the latest visit information of a repository.
    
    Args:
        origin_url: URL of the repository.
        headers: HTTP headers with authorization token.
        
    Returns:
        JSON response with the latest visit information or None if an error occurs.
    """
    url_latest_visit = f"https://archive.softwareheritage.org/api/1/origin/{origin_url}/visit/latest/"
    while True:
        response = requests.get(url_latest_visit, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            logging.error(f"Error 429: Rate limit exceeded. Waiting 60 seconds before retrying...")
            time.sleep(60)
        else:
            logging.error(f"Error {response.status_code} when retrieving the latest visit.")
            return None

# Function to get snapshot information
def get_snapshot_info(snapshot_id, headers):
    """
    Get snapshot information.
    
    Args:
        snapshot_id: ID of the snapshot.
        headers: HTTP headers with authorization token.
        
    Returns:
        JSON response with the snapshot information or None if an error occurs.
    """
    url_snapshot = f"https://archive.softwareheritage.org/api/1/snapshot/{snapshot_id}/"
    while True:
        response = requests.get(url_snapshot, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            logging.error(f"Error 429: Rate limit exceeded. Waiting 60 seconds before retrying...")
            time.sleep(60)
        else:
            logging.error(f"Error {response.status_code} when retrieving the snapshot.")
            return None

# Function to get revision information
def get_revision_info(revision_id, headers):
    """
    Get revision information.
    
    Args:
        revision_id: ID of the revision.
        headers: HTTP headers with authorization token.
        
    Returns:
        JSON response with the revision information or None if an error occurs.
    """
    url_revision = f"https://archive.softwareheritage.org/api/1/revision/{revision_id}/"
    while True:
        response = requests.get(url_revision, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            logging.error(f"Error 429: Rate limit exceeded. Waiting 60 seconds before retrying...")
            time.sleep(60)
        else:
            logging.error(f"Error {response.status_code} when retrieving the revision.")
            return None

# Function to get detailed information about a project
def get_project_info(origin_url, headers):
    """
    Get detailed information about a project.
    
    Args:
        origin_url: URL of the project repository.
        headers: HTTP headers with authorization token.
        
    Returns:
        Dictionary with detailed project information.
    """
    visit_info = get_last_visit_info(origin_url, headers)
    if not visit_info:
        return {}

    snapshot_id = visit_info.get('snapshot')
    snapshot_info = get_snapshot_info(snapshot_id, headers)
    if not snapshot_info:
        return {}

    branches = snapshot_info.get('branches', {})
    revision_id = None
    if "refs/heads/main" in branches:
        revision_id = branches['refs/heads/main']['target']
    else:
        for key in branches:
            if key != 'HEAD':
                revision_id = branches[key]['target']
                break

    revision_info = get_revision_info(revision_id, headers) if revision_id else {}
    
    title = os.path.basename(origin_url).replace('.git', '').replace('_', ' ').replace('-', ' ')

    authors = []
    if revision_info:
        author_name = revision_info.get('author', {}).get('name', 'Unknown')
        author_email = revision_info.get('author', {}).get('email', 'Unknown')
        authors.append({"name": author_name, "mail": author_email})

    project_info = {
        "title": title,
        "authors": authors,
        "sh_id": revision_id,
        "abstract": revision_info.get('message', 'Unknown') if revision_info else 'Unknown',
        "submitted_date": revision_info.get('date', 'Unknown') if revision_info else 'Unknown',
        "updated_date": visit_info.get('date', 'Unknown'),
        "softCodeRepository": origin_url,
        "domain": "",  
        "language": "",
        "laboratory": "",
        "keyword": "",
        "source": "Software_heritage",
    }
    
    return project_info

def main(input_file, output_file, token):
    """
    Main function to fetch project data and save it to a JSON file.
    
    Args:
        input_file: Path to the input JSON file with project URLs.
        output_file: Path to the output JSON file to save project information.
        token: Authorization token for the Software Heritage API.
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    # Load the input file
    try:
        with open(input_file, "r", encoding='utf-8') as file:
            input_data = json.load(file)
            projects = input_data.get("projects", [])
            logging.info(f"{len(projects)} projects loaded from input file.")
    except FileNotFoundError:
        logging.error(f"Input file {input_file} not found.")
        return
    
    # Load existing output file if it exists
    if os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding='utf-8') as file:
                structured_data = json.load(file)
                existing_urls = {project["softCodeRepository"] for project in structured_data["projects"]}
        except json.JSONDecodeError:
            logging.error("Error decoding output file, starting with a new file")
            structured_data = {"number_of_projects": 0, "projects": []}
            existing_urls = set()
    else:
        structured_data = {"number_of_projects": 0, "projects": []}
        existing_urls = set()

    # Process each project in the input file
    for project in projects:
        origin_url = project.get("url", "N/A")
        if origin_url in existing_urls or origin_url == "N/A":
            continue
        
        project_info = get_project_info(origin_url, headers)
        if project_info:
            structured_data["projects"].append(project_info)
            structured_data["number_of_projects"] += 1

            # Save output file after each project
            with open(output_file, "w", encoding='utf-8') as file:
                json.dump(structured_data, file, ensure_ascii=False, indent=4)
            logging.info(f"Project {project_info['title']} added to output file.")

    logging.info(f"Structured data saved in {output_file}")

if __name__ == "__main__":
    input_file = "SH_CNRS_PROJ.json" 
    output_file = "SH_CNRS.json"  
    token = "YOUR_PERSONAL_SH_TOKEN"
    main(input_file, output_file, token)
