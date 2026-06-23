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
    paper="https://journals.sagepub.com/doi/10.1177/02783649231177322",
    citation=r"""@article{boittiaux2023eiffel,
  title   = {Eiffel Tower: A deep-sea underwater dataset for long-term visual localization},
  author  = {Boittiaux, Cl{\'e}mentin and Dune, Claire and Ferrera, Maxime and Arnaubec, Aur{\'e}lien and Marxer, Ricard and Matabos, Marjolaine and Van Audenhaege, Lo{\"i}c and Hugel, Vincent},
  journal = {The International Journal of Robotics Research},
  volume  = {42},
  number  = {9},
  pages   = {689--699},
  year    = {2023},
  publisher = {SAGE Publications},
  doi     = {10.1177/02783649231177322}
}""",
    pose_gt=True,
    image_frames=True,
    downloader=download,
    files=FILES,
)


if __name__ == "__main__":
    download(Path.home() / "Datasets" / "EiffelTower")
