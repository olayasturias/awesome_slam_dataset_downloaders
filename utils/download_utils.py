"""Generic download + extraction helpers shared by every dataset module.

All download helpers accept an optional ``progress_cb(fraction, message)`` where
``fraction`` is overall progress in ``[0, 1]`` across the whole batch. The web UI
uses it to render real progress bars; CLI use can ignore it.
"""
import logging
import os
import tarfile
import zipfile
from typing import Callable, Iterable, Optional
from urllib.parse import urlparse, parse_qs

import requests

logger = logging.getLogger(__name__)

# (overall_fraction in [0, 1], message)
ProgressCb = Callable[[float, str], None]

_CHUNK = 8192


def extract_filename(url: str) -> Optional[str]:
    """Best-effort filename from a URL.

    Handles Seafile-style links that carry the real path in a ``?p=`` query
    parameter (used by the Aqualoc mirror); returns ``None`` otherwise so the
    caller can fall back to the URL path.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if 'p' in query_params:
        file_path = query_params['p'][0]
        return file_path.split('/')[-1]
    return None


def _filename_for(url: str, fallback: Optional[str] = None) -> str:
    extracted = extract_filename(url)
    if extracted:
        return os.path.basename(extracted)
    if fallback:
        return fallback
    name = os.path.basename(urlparse(url).path)
    return name or "download.bin"


def download_file(
    url: str,
    file_path: str,
    on_bytes: Optional[Callable[[int, int], None]] = None,
) -> str:
    """Stream a single URL to ``file_path``.

    ``on_bytes(downloaded, total)`` is called as bytes arrive (``total`` is 0
    when the server sends no ``Content-Length``). Returns ``file_path``.
    """
    logger.info("Downloading %s -> %s", url, file_path)
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total = int(response.headers.get("Content-Length", 0))
    downloaded = 0
    with open(file_path, "wb") as fh:
        for chunk in response.iter_content(chunk_size=_CHUNK):
            if not chunk:
                continue
            fh.write(chunk)
            downloaded += len(chunk)
            if on_bytes:
                on_bytes(downloaded, total)
    logger.info("Downloaded %s (%d bytes)", file_path, downloaded)
    return file_path


def _download_batch(
    items: "list[tuple[str, str]]",
    progress_cb: Optional[ProgressCb] = None,
) -> "list[str]":
    """Download ``(url, file_path)`` pairs, reporting overall progress.

    Overall fraction blends completed files with the current file's byte
    progress: ``(files_done + current_fraction) / total_files``.
    """
    total_files = len(items)
    downloaded_files: "list[str]" = []

    for index, (url, file_path) in enumerate(items):
        def on_bytes(done: int, total: int, _index=index, _url=url):
            if not progress_cb:
                return
            # Clamp: with gzip transfer-encoding the decoded byte count can
            # exceed the (compressed) Content-Length, pushing the ratio past 1.
            file_frac = min(1.0, done / total) if total else 0.0
            overall = min(1.0, (_index + file_frac) / total_files)
            progress_cb(overall, f"Downloading {os.path.basename(file_path)}")

        try:
            download_file(url, file_path, on_bytes=on_bytes)
            downloaded_files.append(file_path)
        except requests.RequestException as exc:
            logger.error("Failed to download %s: %s", url, exc)
        if progress_cb:
            progress_cb((index + 1) / total_files, f"Downloaded {os.path.basename(file_path)}")

    return downloaded_files


def download_files(
    urls: Iterable[str],
    output_folder: str,
    progress_cb: Optional[ProgressCb] = None,
    names: "Optional[dict[str, str]]" = None,
) -> "list[str]":
    """Download raw files (no extraction) into ``output_folder``.

    ``names`` optionally maps a URL to a desired local filename.
    """
    os.makedirs(output_folder, exist_ok=True)
    names = names or {}
    items = [
        (url, os.path.join(output_folder, names.get(url, _filename_for(url))))
        for url in urls
    ]
    return _download_batch(items, progress_cb)


def download_tar_gz_files(
    urls: Iterable[str],
    output_folder: str,
    progress_cb: Optional[ProgressCb] = None,
) -> "list[str]":
    """Download a list of .tar/.tar.gz files into ``output_folder``."""
    return download_files(urls, output_folder, progress_cb=progress_cb)


def download_zip_dict(
    urls: dict,
    output_folder: str,
    progress_cb: Optional[ProgressCb] = None,
) -> "list[str]":
    """Download ``{key: url}`` files, naming each local file ``<key>.zip``."""
    os.makedirs(output_folder, exist_ok=True)
    items = [
        (url, os.path.join(output_folder, f"{key}.zip"))
        for key, url in urls.items()
    ]
    return _download_batch(items, progress_cb)


def extract_tar_gz_file(file_paths: Iterable[str], output_folder: str) -> None:
    """Extract .tar / .tar.gz / .tgz archives into ``output_folder``."""
    for file_path in file_paths:
        if not os.path.exists(file_path):
            logger.warning("File not found: %s", file_path)
            continue
        if file_path.endswith('.tar.gz') or file_path.endswith('.tgz'):
            mode = 'r:gz'
        elif file_path.endswith('.tar'):
            mode = 'r'
        else:
            logger.warning("Unsupported tar file type: %s", file_path)
            continue
        try:
            with tarfile.open(file_path, mode) as tar:
                tar.extractall(path=output_folder)
            logger.info("Extracted %s -> %s", file_path, output_folder)
        except Exception as exc:  # noqa: BLE001 - report and continue with the rest
            logger.error("Failed to extract %s: %s", file_path, exc)


def extract_zip_files(zip_files: Iterable[str], output_folder: str) -> None:
    """Extract a list of .zip files into ``output_folder``."""
    os.makedirs(output_folder, exist_ok=True)
    for zip_path in zip_files:
        if not zipfile.is_zipfile(zip_path):
            logger.warning("Skipping non-zip file: %s", zip_path)
            continue
        logger.info("Extracting %s -> %s", zip_path, output_folder)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_folder)


def download_and_extract_grouped(
    items: "Iterable[tuple[str, str]]",
    output_folder: str,
    progress_cb: Optional[ProgressCb] = None,
) -> "list[str]":
    """Download ``(url, subfolder)`` tar archives, extracting each into its own
    ``output_folder/subfolder``. Used by datasets split into per-trial folders.
    """
    items = list(items)
    total = len(items)
    produced: "list[str]" = []
    for index, (url, subfolder) in enumerate(items):
        dest = os.path.join(output_folder, str(subfolder))
        os.makedirs(dest, exist_ok=True)

        def on_overall(frac: float, msg: str, _i=index):
            if progress_cb:
                progress_cb((_i + frac) / total, msg)

        downloaded = download_tar_gz_files([url], dest, progress_cb=on_overall)
        extract_tar_gz_file(downloaded, dest)
        produced.extend(downloaded)
    return produced
