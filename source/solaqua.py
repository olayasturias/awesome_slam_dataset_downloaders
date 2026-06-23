"""SOLAQUA -- SINTEF Ocean Large Aquaculture Robotics Dataset.

Underwater fish-farm robotics dataset (navigation, sonar, mono/stereo cameras,
vehicle telemetry) delivered as ROS bag files. arXiv:2504.01790.

NOTE ON ACCESS
--------------
The data is hosted on the SINTEF data portal (a JavaScript single-page app) and
its file endpoints are access-controlled -- anonymous requests to the public
API return HTTP 401. The per-file download URLs therefore cannot be hard-coded
here yet. To enable downloading, resolve the real ``*_data.bag`` / ``*_video.bag``
URLs and add them to ``BAG_URLS`` below:

  1. Open the feature page in a browser and inspect the network/XHR calls that
     fire when you click a file (DevTools -> Network), OR
  2. Use the official SDK -- ``pip install data-sintef-api`` -- with an API token
     to list and resolve file download URLs for the feature id.

Once ``BAG_URLS`` is populated the existing code path downloads the raw bags
(no extraction needed).
"""
from pathlib import Path
from typing import Optional

from source.base import Dataset, ProgressCb
from utils.download_utils import download_files

FEATURE_URL = "https://data.sintef.no/feature/fe-a8f86232-5107-495e-a3dd-a86460eebef6"

# TODO: populate with resolved ROS bag download URLs (see module docstring).
BAG_URLS: "list[str]" = []


def download(output_folder: Path, progress_cb: Optional[ProgressCb] = None) -> "list[str]":
    if not BAG_URLS:
        raise NotImplementedError(
            "SOLAQUA download URLs are not configured. The SINTEF data portal "
            "gates file access (HTTP 401 for anonymous API requests). Resolve the "
            f"ROS bag URLs from {FEATURE_URL} (browser DevTools or the "
            "`data-sintef-api` SDK with an API token) and add them to "
            "source/solaqua.py::BAG_URLS."
        )
    return download_files(BAG_URLS, str(output_folder), progress_cb=progress_cb)


SOLAQUA = Dataset(
    name="SOLAQUA",
    category="Underwater",
    description="SINTEF Ocean Large Aquaculture Robotics Dataset: net-following, "
                "manual-control and calibration sequences recorded by an underwater "
                "robot in an operational fish farm (63 sequences total).",
    modalities="Mono + stereo cameras, multibeam sonar, DVL, USBL, IMU, baro",
    data_format="ROS bag",
    homepage=FEATURE_URL,
    paper="https://arxiv.org/abs/2504.01790",
    citation=r"""@misc{ohrem2025solaqua,
  title         = {SOLAQUA: SINTEF Ocean Large Aquaculture Robotics Dataset},
  author        = {Ohrem, Sveinung Johan and Haugal{\o}kken, Bent and Kelasidi, Eleni},
  year          = {2025},
  eprint        = {2504.01790},
  archivePrefix = {arXiv},
  primaryClass  = {cs.RO}
}""",
    license="CC BY-SA 4.0",
    pose_gt=True,
    image_frames=True,
    # Listed in the UI but currently raises a clear message until BAG_URLS is set.
    released=True,
    downloader=download,
)


if __name__ == "__main__":
    download(Path.home() / "Datasets" / "SOLAQUA")
