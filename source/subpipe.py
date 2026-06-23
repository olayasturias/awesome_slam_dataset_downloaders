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
    paper="https://arxiv.org/abs/2401.17907",
    citation=r"""@inproceedings{alvareztunon2024subpipe,
  author    = {{\'A}lvarez-Tu{\~n}{\'o}n, Olaya and Marnet, Luiza Ribeiro and Antal, L{\'a}szl{\'o} and Aubard, Martin and Costa, Maria and Brodskiy, Yury},
  title     = {{SubPipe}: A Submarine Pipeline Inspection Dataset for Segmentation and Visual-inertial Localization},
  booktitle = {OCEANS 2024 - Singapore},
  year      = {2024},
  pages     = {1--7},
  publisher = {IEEE},
  doi       = {10.1109/OCEANS51537.2024.10682150}
}""",
    pose_gt=True,
    image_frames=True,
    downloader=download,
    files=FILES,
)


if __name__ == "__main__":
    download(Path.home() / "Datasets" / "SubPipe")
