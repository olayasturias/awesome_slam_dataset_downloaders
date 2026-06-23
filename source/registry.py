"""Single source of truth: every dataset known to this repo.

Both the web UI (``web_downloader.py``) and the documentation are driven by this
list. To add a dataset, build a ``Dataset`` in a ``source/<name>.py`` module and
append it here -- nothing else needs editing.
"""
from source.aqualoc import AQUALOC_ARCHAEOLOGICAL, AQUALOC_HARBOR
from source.base import Dataset
from source.eiffel_tower import EIFFEL_TOWER
from source.solaqua import SOLAQUA
from source.sotrue import SOTRUE
from source.sovis import SOVIS
from source.subpipe import SUBPIPE

DATASETS: "list[Dataset]" = [
    SUBPIPE,
    SOTRUE,
    EIFFEL_TOWER,
    AQUALOC_ARCHAEOLOGICAL,
    AQUALOC_HARBOR,
    SOLAQUA,
    SOVIS,
]
