# awesome_slam_dataset_downloaders

A curated collection of **SLAM-related datasets** together with **ready-to-use Python scripts** to download and extract them quickly and consistently on your local machine.

The goal of this repository is to:
- Centralize links to high-quality SLAM datasets
- Provide **reproducible download scripts**
- Avoid manual clicks, broken links, and ad-hoc extraction steps
- Serve as a lightweight utility repo that can be reused across projects

---

## Supported Domains
- Visual SLAM
- Visual–Inertial SLAM
- Underwater SLAM
- Multi-session / long-term mapping datasets

---

## Underwater Datasets

| Dataset                                                                            | Pose GT | Image Frames | Modalities                                        | Format          |
|------------------------------------------------------------------------------------|---------|--------------|---------------------------------------------------|-----------------|
| [**AQUALOC**](https://www.aqualoc.org/)                                            | yes     | yes          | Mono camera, IMU, pressure                        | tar.gz          |
| [**SubPipe**](https://github.com/remaro-network/SubPipe-dataset)                   | yes     | yes          | Mono camera                                       | zip             |
| [**EiffelTower**](https://www.seanoe.org/data/00810/92226/)                        | yes     | yes          | Mono camera                                       | zip             |
| **SOTRUE**                                                                         | –       | yes          | Camera images                                     | tar (images)    |
| [**SOLAQUA**](https://data.sintef.no/feature/fe-a8f86232-5107-495e-a3dd-a86460eebef6) | yes     | yes          | Mono+stereo cameras, multibeam sonar, DVL, USBL, IMU | ROS bag      |
| [**SOVIS**](https://arxiv.org/abs/2606.01398) *(data not yet released)*            | –       | yes          | Mono camera + multibeam sonar                     | ROS 2 bag + H.264 |

### Dataset Notes
- **AQUALOC**
  Large-scale underwater visual SLAM dataset with archaeological and harbor scenarios.
  Provides camera trajectories, raw images, and challenging lighting/turbidity conditions.

- **SubPipe**
  Pipeline inspection dataset focused on structured underwater environments with ground truth trajectories.

- **EiffelTower**
  Multi-year underwater survey dataset (2015–2020) around the Eiffel Tower foundations.
  Suitable for long-term SLAM, temporal change analysis, and relocalization.

- **SOTRUE**
  Underwater images captured across graded turbidity levels (turbid0–turbid5) with
  repeated trials, for robustness and image-restoration studies.

- **SOLAQUA**
  SINTEF Ocean Large Aquaculture Robotics Dataset ([arXiv:2504.01790](https://arxiv.org/abs/2504.01790)).
  63 sequences (calibration / manual-control / net-following) recorded by an underwater
  robot in an operational fish farm, delivered as ROS bag files. License CC BY-SA 4.0.
  **Access note:** the SINTEF data portal gates file downloads (anonymous API requests
  return HTTP 401), so the per-file ROS bag URLs must be resolved (browser DevTools or
  the `data-sintef-api` SDK with an API token) and added to `source/solaqua.py::BAG_URLS`
  before the downloader works.

- **SOVIS**
  Sonar-visual cross-modal underwater perception dataset ([arXiv:2606.01398](https://arxiv.org/abs/2606.01398)):
  ~76,600 paired multibeam-sonar/camera frames over 17 dives at six Trondheimfjord sites.
  **No public download link has been released yet** — contact the authors
  (`weitung@mit.edu`, `phil.tinn@sintef.no`). Listed here so it is documented and ready
  to wire up once published.

---

## Repository Structure

```text
awesome_slam_dataset_downloaders/
├── utils/
│   ├── download_utils.py     # Generic download + extraction utilities (with progress + logging)
│   └── __init__.py
├── source/
│   ├── base.py               # Dataset abstraction + uniform download() entry point
│   ├── registry.py           # Central DATASETS list (drives UI + docs)
│   ├── aqualoc.py
│   ├── eiffel_tower.py
│   ├── subpipe.py
│   ├── sotrue.py
│   ├── solaqua.py
│   └── sovis.py
├── docs/                     # Static GitHub Pages site (generated)
│   ├── index.html
│   └── datasets.json
├── media/                    # preview.png for the README
├── build_site.py             # Generates docs/ from the dataset registry
├── web_downloader.py         # Flask + pywebview desktop UI
├── requirements.txt
└── README.md
```

---

## Online Dataset Browser (GitHub Pages)

A static website lists every dataset with **direct download links**:

**https://olayasturias.github.io/awesome_slam_dataset_downloaders/**

The buttons link straight to each dataset's host (Zenodo, SEANOE, Wasabi, Seafile, …),
so your browser downloads from the origin. Because GitHub Pages is static, the online
site only links — it does **not** download-and-extract for you. For that, use the local
web downloader or CLI below.

The site is generated from the dataset registry into `docs/`:

```powershell
python build_site.py        # writes docs/index.html + docs/datasets.json
```

Re-run it whenever you add or change a dataset, then commit `docs/`. GitHub Pages is
configured to serve the `/docs` folder on the `main` branch
(Settings → Pages → Source: *Deploy from a branch* → `main` / `/docs`).

---

## Web Downloader Interface

![Web Downloader Interface Preview](media/preview.png)

A simple web interface is included for selecting and downloading datasets interactively.

### Features
- Select one or more datasets to download using checkboxes
- Choose the local download folder using a folder picker
- See **real** download progress (overall percentage + current file)
- Stop downloads at any time
- Datasets without a public download yet (e.g. SOVIS) are shown disabled
- Uses the Vapor theme from Bootswatch for a modern look

### How to Run

1. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Start the web downloader**
   ```powershell
   python web_downloader.py
   ```

3. **Usage**
   - The web interface will open automatically.
   - Select datasets and a download folder.
   - Click "Download" to start.
   - Monitor progress and stop downloads if needed.

> **Note:** The interface is cross-platform and works on Windows, macOS, and Linux.

---

## Command-Line Usage

Each dataset module is runnable directly (downloads into `~/Datasets/<name>`):

```powershell
python -m source.subpipe
python -m source.eiffel_tower
python -m source.sotrue
python -m source.aqualoc
```

Or call a dataset programmatically via the registry:

```python
from source.registry import DATASETS

dataset = next(d for d in DATASETS if d.name == "SubPipe")
dataset.download("/path/to/output")          # str or Path
# optional progress: dataset.download(path, progress_cb=lambda frac, msg: print(frac, msg))
```

---

## Adding a New Dataset

The web UI and docs are driven by a single registry, so adding a dataset is two steps:

1. **Create `source/<name>.py`** with a download function and a `Dataset` instance:

   ```python
   from pathlib import Path
   from typing import Optional

   from source.base import Dataset, ProgressCb
   from utils.download_utils import download_zip_dict, extract_zip_files

   URLS = {"MyDataset": "https://example.com/mydataset.zip"}

   def download(output_folder: Path, progress_cb: Optional[ProgressCb] = None) -> "list[str]":
       files = download_zip_dict(URLS, str(output_folder), progress_cb=progress_cb)
       extract_zip_files(files, str(output_folder))
       return files

   MY_DATASET = Dataset(
       name="MyDataset",
       category="Underwater",
       description="…",
       modalities="Mono camera",
       data_format="zip",
       homepage="https://example.com",
       downloader=download,
   )
   ```

   Available helpers in `utils/download_utils.py`: `download_files` (raw files, no
   extraction — e.g. ROS bags), `download_zip_dict` + `extract_zip_files`,
   `download_tar_gz_files` + `extract_tar_gz_file`, and `download_and_extract_grouped`
   (one archive per sub-folder). All accept the optional `progress_cb`.

2. **Register it** in `source/registry.py` by importing the instance and appending it
   to `DATASETS`. That's it — it now appears in the web UI and CLI.

   For datasets whose data is not public yet, set `released=False` and
   `downloader=None`; they render disabled in the UI.

---
