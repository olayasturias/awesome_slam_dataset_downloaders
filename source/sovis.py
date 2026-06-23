"""SOVIS -- a sonar-visual dataset for cross-modal underwater robot perception.

Oculus M750d multibeam sonar + 1080p mono camera, ~76,600 paired frames across
17 dives at 6 Trondheimfjord sites. arXiv:2606.01398 (ICRA 2026 S2S Workshop).

No public download link has been released as of June 2026. This entry exists so
the dataset is documented and ready to wire up once the data is published.
Contact the authors (weitung@mit.edu, phil.tinn@sintef.no) for access.
"""
from source.base import Dataset

PAPER_URL = "https://arxiv.org/abs/2606.01398"

# released=False -> Dataset.download() raises NotImplementedError and the web UI
# renders it disabled. Set the downloader + released=True once data is published.
SOVIS = Dataset(
    name="SOVIS",
    category="Underwater",
    description="Sonar-visual dataset for cross-modal underwater perception: "
                "~76.6k paired multibeam-sonar/camera frames over 17 dives at six "
                "Trondheimfjord sites. Data not yet publicly released.",
    modalities="Mono camera + multibeam sonar (Oculus M750d)",
    data_format="ROS 2 bag (sonar) + H.264 (video)",
    paper=PAPER_URL,
    image_frames=True,
    released=False,
    downloader=None,
)
