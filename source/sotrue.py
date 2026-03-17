import os
from utils.download_utils import download_tar_gz_files, extract_tar_gz_file


TAR_FILES = [
    ("https://s3.us-west-1.wasabisys.com/sotrue/turbid0_trial1_images.tar", "turbid0/trial1"),
    ("https://s3.us-west-1.wasabisys.com/sotrue/turbid2_trial2_images.tar", "turbid0/trial2"),
    ("https://s3.us-west-1.wasabisys.com/sotrue/turbid1_trial1_images.tar", "turbid1/trial1"),
    ("https://s3.us-west-1.wasabisys.com/sotrue/turbid1_trial2_images.tar", "turbid1/trial2"),
    ("https://s3.us-west-1.wasabisys.com/sotrue/turbid2_trial1_images.tar", "turbid2/trial1"),
    ("https://s3.us-west-1.wasabisys.com/sotrue/turbid2_trial2_images.tar", "turbid2/trial2"),
    ("https://s3.us-west-1.wasabisys.com/sotrue/turbid3_trial1_images.tar", "turbid3/trial1"),
    ("https://s3.us-west-1.wasabisys.com/sotrue/turbid3_trial2_images.tar", "turbid3/trial2"),
    ("https://s3.us-west-1.wasabisys.com/sotrue/turbid4_trial1_images.tar", "turbid4/trial1"),
    ("https://s3.us-west-1.wasabisys.com/sotrue/turbid4_trial2_images.tar", "turbid4/trial2"),
    ("https://s3.us-west-1.wasabisys.com/sotrue/turbid5_trial1_images.tar", "turbid5/trial1"),
    ("https://s3.us-west-1.wasabisys.com/sotrue/turbid5_trial2_images.tar", "turbid5/trial2"),
]


def download_and_extract_tar_files(output_directory):
    for url, folder in TAR_FILES:
        full_folder = os.path.join(output_directory, str(folder))  # Ensure folder is str
        os.makedirs(full_folder, exist_ok=True)
        print(f"Downloading {url} to {full_folder}")
        downloaded = download_tar_gz_files([url], full_folder)
        print(f"Extracting {downloaded} to {full_folder}")
        extract_tar_gz_file(downloaded, full_folder)


if __name__ == "__main__":
    output_dir = r"C:\Users\oat\Datasets\SOTRUE"
    download_and_extract_tar_files(output_dir)
