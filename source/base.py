"""Core dataset abstraction shared by every downloader.

A :class:`Dataset` bundles the metadata shown in the README / web UI together
with a single, uniform ``download`` entry point. Individual ``source/*.py``
modules build one (or more) ``Dataset`` instances and register them in
``source/registry.py`` -- that single list drives both the web interface and
the documentation, so adding a dataset never means editing the UI again.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from os.path import basename
from typing import Callable, Optional
from urllib.parse import urlparse

# Progress callback: (overall_fraction in [0, 1], human-readable message).
ProgressCb = Callable[[float, str], None]

# A downloader receives the (already-created) output folder and an optional
# progress callback, and returns the list of paths it produced on disk.
Downloader = Callable[[Path, Optional[ProgressCb]], "list[str]"]


@dataclass
class DatasetFile:
    """One downloadable file/archive of a dataset.

    Exposing the raw URLs as data (rather than burying them in a downloader
    closure) lets the same list drive the CLI downloader *and* the static
    GitHub Pages site, which links straight to these URLs.
    """

    url: str
    label: str = ""        # display name; falls back to the URL filename
    subfolder: str = ""    # save/extract target relative to the output folder

    @property
    def display(self) -> str:
        return self.label or basename(urlparse(self.url).path) or self.url


@dataclass
class Dataset:
    """A downloadable SLAM dataset plus the metadata describing it."""

    name: str
    category: str  # e.g. "Underwater", "Visual-Inertial"
    description: str
    modalities: str = ""          # e.g. "Mono + sonar, IMU"
    data_format: str = ""         # e.g. "ROS bag", "tar (images)", "zip"
    homepage: str = ""
    paper: str = ""
    citation: str = ""           # BibTeX entry for the dataset's paper
    license: str = ""
    pose_gt: bool = False         # ground-truth poses available?
    image_frames: bool = False    # image frames available?
    released: bool = True         # is the data publicly downloadable yet?
    downloader: Optional[Downloader] = None
    files: "list[DatasetFile]" = field(default_factory=list)  # direct download URLs

    def download(self, output_folder, progress_cb: Optional[ProgressCb] = None) -> "list[str]":
        """Download the dataset into ``output_folder``.

        ``output_folder`` may be a ``str`` or ``Path`` -- it is normalized and
        created here, so downloaders never have to. Raises
        ``NotImplementedError`` for datasets that are not yet downloadable.
        """
        if self.downloader is None or not self.released:
            raise NotImplementedError(
                f"{self.name} has no public downloader yet. "
                f"See {self.homepage or self.paper or 'the dataset homepage'}."
            )
        out = Path(output_folder)
        out.mkdir(parents=True, exist_ok=True)
        return self.downloader(out, progress_cb)
