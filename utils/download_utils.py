import os
import requests
import zipfile
from typing import Iterable
from urllib.parse import urlparse, parse_qs


def extract_filename(url):
    """
    Extracts the filename from the given URL.

    Args:
        url (str): The URL to extract the filename from.

    Returns:
        str: The extracted filename, or None if not found.
    """
    response = requests.get(url, stream=True)
    print(f"Status code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")

    # Parse the URL
    parsed_url = urlparse(url)

    # Extract the query parameters
    query_params = parse_qs(parsed_url.query)

    # Check if 'p' parameter exists and retrieve the last part as the filename
    if 'p' in query_params:
        file_path = query_params['p'][0]  # Get the first value of the 'p' parameter
        return file_path.split('/')[-1]  # Extract the filename
    return None


def download_tar_gz_files(urls, output_folder):
    """
    Downloads a list of .tar.gz files from the given URLs to a local folder.

    Args:
        urls (list): A list of URLs pointing to .tar.gz files.
        output_folder (str): The local folder where the files will be saved.

    Returns:
        list: A list of file paths to the downloaded files.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    downloaded_files = []

    for url in urls:
        try:
            # Try to extract filename from URL query, else fallback to URL path
            extracted = extract_filename(url)
            if extracted:
                file_name = os.path.basename(extracted)
            else:
                file_name = os.path.basename(url)

            # Local file path
            file_path = os.path.join(output_folder, file_name)

            # Download the file
            print(f"Downloading {url} to {file_path}")
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an error for bad status codes

            # Write the file to the local directory
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            downloaded_files.append(file_path)
            print(f"Downloaded: {file_path}")

        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")

    return downloaded_files


def extract_tar_gz_file(file_paths, output_folder):
    """
    Extracts a .tar.gz file to the specified output folder.

    Args:
        file_path (list): The list of paths to the .tar.gz file.
        output_folder (str): The folder where the contents will be extracted.
    """
    import tarfile
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        try:
            # Detect file type and open accordingly
            if file_path.endswith('.tar.gz') or file_path.endswith('.tgz'):
                mode = 'r:gz'
            elif file_path.endswith('.tar'):
                mode = 'r'
            else:
                print(f"Unsupported tar file type: {file_path}")
                continue
            with tarfile.open(file_path, mode) as tar:
                tar.extractall(path=output_folder)
                print(f"Extracted {file_path} to {output_folder}")
        except Exception as e:
            print(f"Failed to extract {file_path}: {e}")

def extract_zip_files(zip_files: Iterable[str], output_folder: str) -> None:
    """
    Extracts a list of .zip files into the given output folder.

    Args:
        zip_files (Iterable[str]): Paths to .zip files.
        output_folder (str): Directory where files will be extracted.
    """
    os.makedirs(output_folder, exist_ok=True)

    for zip_path in zip_files:
        if not zipfile.is_zipfile(zip_path):
            print(f"Skipping non-zip file: {zip_path}")
            continue

        print(f"Extracting {zip_path} to {output_folder}")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_folder)


def download_zip_dict(urls: dict, output_folder: str) -> list[str]:
    """
    Downloads a dictionary of .zip files to a local folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    downloaded_files = []

    for key, url in urls.items():
        try:
            file_name = f"{key}.zip"
            file_path = os.path.join(output_folder, file_name)

            print(f"Downloading {url} → {file_path}")
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            downloaded_files.append(file_path)
            print(f"Downloaded: {file_path}")

        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")

    return downloaded_files