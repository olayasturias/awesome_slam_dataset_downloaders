"""SubPipe -- underwater pipeline-inspection dataset (Zenodo)."""
from pathlib import Path
from typing import Optional

from source.base import Dataset, DatasetFile, ProgressCb
from utils.download_utils import download_files, extract_zip_files

FILES = [
    DatasetFile("https://zenodo.org/records/12666132/files/SubPipe.zip?download=1", "SubPipe.zip"),
]


def download(output_folder: Path, progress_cb: Optional[ProgressCb] = None) -> "list[str]":
    files = download_files([f.url for f in FILES], str(output_folder), progress_cb=progress_cb)
    extract_zip_files(files, str(output_folder))
    return files


SUBPIPE = Dataset(
    name="SubPipe",
    category="Underwater",
    description="Pipeline inspection dataset focused on structured underwater "
                "environments with ground-truth trajectories.",
    modalities="Mono camera",
    data_format="zip",
    homepage="https://github.com/remaro-network/SubPipe-dataset",
    pose_gt=True,
    image_frames=True,
    downloader=download,
    files=FILES,
)


if __name__ == "__main__":
    download(Path.home() / "Datasets" / "SubPipe")
