"""SOTRUE -- underwater images across graded turbidity levels (Wasabi S3)."""
from pathlib import Path
from typing import Optional

from source.base import Dataset, DatasetFile, ProgressCb
from utils.download_utils import download_and_extract_grouped

_BASE = "https://s3.us-west-1.wasabisys.com/sotrue"

FILES = [
    DatasetFile(f"{_BASE}/turbid0_trial1_images.tar", "turbid0 trial1", "turbid0/trial1"),
    DatasetFile(f"{_BASE}/turbid2_trial2_images.tar", "turbid0 trial2", "turbid0/trial2"),
    DatasetFile(f"{_BASE}/turbid1_trial1_images.tar", "turbid1 trial1", "turbid1/trial1"),
    DatasetFile(f"{_BASE}/turbid1_trial2_images.tar", "turbid1 trial2", "turbid1/trial2"),
    DatasetFile(f"{_BASE}/turbid2_trial1_images.tar", "turbid2 trial1", "turbid2/trial1"),
    DatasetFile(f"{_BASE}/turbid2_trial2_images.tar", "turbid2 trial2", "turbid2/trial2"),
    DatasetFile(f"{_BASE}/turbid3_trial1_images.tar", "turbid3 trial1", "turbid3/trial1"),
    DatasetFile(f"{_BASE}/turbid3_trial2_images.tar", "turbid3 trial2", "turbid3/trial2"),
    DatasetFile(f"{_BASE}/turbid4_trial1_images.tar", "turbid4 trial1", "turbid4/trial1"),
    DatasetFile(f"{_BASE}/turbid4_trial2_images.tar", "turbid4 trial2", "turbid4/trial2"),
    DatasetFile(f"{_BASE}/turbid5_trial1_images.tar", "turbid5 trial1", "turbid5/trial1"),
    DatasetFile(f"{_BASE}/turbid5_trial2_images.tar", "turbid5 trial2", "turbid5/trial2"),
]


def download(output_folder: Path, progress_cb: Optional[ProgressCb] = None) -> "list[str]":
    items = [(f.url, f.subfolder) for f in FILES]
    return download_and_extract_grouped(items, str(output_folder), progress_cb=progress_cb)


SOTRUE = Dataset(
    name="SOTRUE",
    category="Underwater",
    description="Underwater image dataset captured across graded turbidity levels "
                "(turbid0-turbid5), each with repeated trials, for robustness studies.",
    modalities="Camera images",
    data_format="tar (images)",
    paper="https://doi.org/10.23919/OCEANS59106.2025.11245072",
    citation=r"""@inproceedings{marburg2025sotrue,
  author    = {Marburg, Aaron and Micatka, Marc},
  title     = {A Dataset for the Assessment of Underwater {SLAM} Degradation in Turbid Water},
  booktitle = {OCEANS 2025 - Great Lakes},
  year      = {2025},
  month     = sep,
  pages     = {1--5},
  address   = {Chicago, IL, USA},
  publisher = {IEEE},
  doi       = {10.23919/OCEANS59106.2025.11245072},
  note      = {Introduces the Stereo Observations in TuRbid Underwater Environments (SOTRUE) dataset}
}""",
    image_frames=True,
    downloader=download,
    files=FILES,
)


if __name__ == "__main__":
    download(Path.home() / "Datasets" / "SOTRUE")
