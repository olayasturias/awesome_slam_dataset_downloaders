from pathlib import Path
from utils.download_utils import download_tar_gz_files, extract_tar_gz_file

ARCHAEO_URLS = [
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FArchaeological_site_sequences%2Farchaeo_sequence_1_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FArchaeological_site_sequences%2Farchaeo_sequence_2_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FArchaeological_site_sequences%2Farchaeo_sequence_3_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FArchaeological_site_sequences%2Farchaeo_sequence_4_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FArchaeological_site_sequences%2Farchaeo_sequence_5_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FArchaeological_site_sequences%2Farchaeo_sequence_6_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FArchaeological_site_sequences%2Farchaeo_sequence_7_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FArchaeological_site_sequences%2Farchaeo_sequence_8_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FArchaeological_site_sequences%2Farchaeo_sequence_9_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FArchaeological_site_sequences%2Farchaeo_sequence_10_raw_data.tar.gz&dl=1",
]

HARBOR_URLS = [
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FHarbor_sites_sequences%2Fharbor_sequence_01_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FHarbor_sites_sequences%2Fharbor_sequence_02_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FHarbor_sites_sequences%2Fharbor_sequence_03_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FHarbor_sites_sequences%2Fharbor_sequence_04_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FHarbor_sites_sequences%2Fharbor_sequence_05_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FHarbor_sites_sequences%2Fharbor_sequence_06_raw_data.tar.gz&dl=1",
    "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2FHarbor_sites_sequences%2Fharbor_sequence_07_raw_data.tar.gz&dl=1"
]

def download_site(urls: list[str], output_folder: Path) -> list[str]:
    output_folder.mkdir(parents=True, exist_ok=True)
    return download_tar_gz_files(urls, str(output_folder))

def download_aqualoc_archaeological_site_sequences(output_folder: Path) -> list[str]:
    return download_site(ARCHAEO_URLS, output_folder)

def download_aqualoc_harbor_site_sequences(output_folder: Path) -> list[str]:
    return download_site(HARBOR_URLS, output_folder)

if __name__ == "__main__":
    root = Path(r"D:\Datasets\Aqualoc2")

    arch_dir = root / "Archaeological_site_sequences"
    downloaded = download_aqualoc_archaeological_site_sequences(arch_dir)
    extract_tar_gz_file(downloaded, str(arch_dir))

    harbor_dir = root / "Harbor_sites_sequences"
    downloaded = download_aqualoc_harbor_site_sequences(harbor_dir)
    extract_tar_gz_file(downloaded, str(harbor_dir))
