"""Aqualoc -- underwater visual SLAM dataset (archaeological + harbor sites)."""
from pathlib import Path
from typing import Optional

from source.base import Dataset, DatasetFile, ProgressCb
from utils.download_utils import download_tar_gz_files, extract_tar_gz_file

_SEAFILE = "https://seafile.lirmm.fr/d/79b03788f29148ca84e5/files/?p=%2F"

ARCHAEO_FILES = [
    DatasetFile(
        f"{_SEAFILE}Archaeological_site_sequences%2Farchaeo_sequence_{i}_raw_data.tar.gz&dl=1",
        f"archaeo_sequence_{i}",
    )
    for i in range(1, 11)
]

HARBOR_FILES = [
    DatasetFile(
        f"{_SEAFILE}Harbor_sites_sequences%2Fharbor_sequence_{i:02d}_raw_data.tar.gz&dl=1",
        f"harbor_sequence_{i:02d}",
    )
    for i in range(1, 8)
]


def _download_site(files: "list[DatasetFile]", output_folder: Path,
                   progress_cb: Optional[ProgressCb]) -> "list[str]":
    downloaded = download_tar_gz_files([f.url for f in files], str(output_folder),
                                       progress_cb=progress_cb)
    extract_tar_gz_file(downloaded, str(output_folder))
    return downloaded


def download_archaeological(output_folder: Path,
                            progress_cb: Optional[ProgressCb] = None) -> "list[str]":
    return _download_site(ARCHAEO_FILES, output_folder, progress_cb)


def download_harbor(output_folder: Path,
                    progress_cb: Optional[ProgressCb] = None) -> "list[str]":
    return _download_site(HARBOR_FILES, output_folder, progress_cb)


AQUALOC_ARCHAEOLOGICAL = Dataset(
    name="Aqualoc Archaeological Site",
    category="Underwater",
    description="Large-scale underwater visual SLAM sequences at deep archaeological "
                "sites, with camera trajectories and challenging turbidity/lighting.",
    modalities="Mono camera, IMU, pressure",
    data_format="tar.gz",
    homepage="https://www.aqualoc.org/",
    pose_gt=True,
    image_frames=True,
    downloader=download_archaeological,
    files=ARCHAEO_FILES,
)

AQUALOC_HARBOR = Dataset(
    name="Aqualoc Harbor Site",
    category="Underwater",
    description="Shallow-water harbor sequences of the Aqualoc visual SLAM dataset, "
                "with camera trajectories and challenging turbidity/lighting.",
    modalities="Mono camera, IMU, pressure",
    data_format="tar.gz",
    homepage="https://www.aqualoc.org/",
    pose_gt=True,
    image_frames=True,
    downloader=download_harbor,
    files=HARBOR_FILES,
)


if __name__ == "__main__":
    root = Path.home() / "Datasets" / "Aqualoc"
    download_archaeological(root / "Archaeological_site_sequences")
    download_harbor(root / "Harbor_sites_sequences")
