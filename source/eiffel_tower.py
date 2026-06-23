"""EiffelTower -- multi-year underwater survey dataset (SEANOE, 2015-2020)."""
from pathlib import Path
from typing import Optional

from source.base import Dataset, DatasetFile, ProgressCb
from utils.download_utils import download_files, extract_zip_files

FILES = [
    DatasetFile("https://www.seanoe.org/data/00810/92226/data/98240.zip", "2015"),
    DatasetFile("https://www.seanoe.org/data/00810/92226/data/98289.zip", "2016"),
    DatasetFile("https://www.seanoe.org/data/00810/92226/data/98314.zip", "2018"),
    DatasetFile("https://www.seanoe.org/data/00810/92226/data/98356.zip", "2020"),
]


def download(output_folder: Path, progress_cb: Optional[ProgressCb] = None) -> "list[str]":
    files = download_files([f.url for f in FILES], str(output_folder), progress_cb=progress_cb)
    extract_zip_files(files, str(output_folder))
    return files


EIFFEL_TOWER = Dataset(
    name="EiffelTower",
    category="Underwater",
    description="Multi-year underwater survey (2015-2020) around the Eiffel Tower "
                "deep-sea vent. Suitable for long-term SLAM, temporal change "
                "analysis, and relocalization.",
    modalities="Mono camera",
    data_format="zip",
    homepage="https://www.seanoe.org/data/00810/92226/",
    pose_gt=True,
    image_frames=True,
    downloader=download,
    files=FILES,
)


if __name__ == "__main__":
    download(Path.home() / "Datasets" / "EiffelTower")
