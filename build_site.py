"""Generate the static GitHub Pages site (docs/index.html) from the registry.

GitHub Pages is static-only, so there is no server-side download/extract. Each
dataset card links straight to the real file hosts (Zenodo, SEANOE, Wasabi,
Seafile); the browser downloads from the origin. Run this whenever datasets
change, then commit docs/.

    python build_site.py
"""
import html
import json
from pathlib import Path

from source.registry import DATASETS

REPO_URL = "https://github.com/olayasturias/awesome_slam_dataset_downloaders"
DOCS = Path(__file__).parent / "docs"

CSS = """
:root{--bg:#221c2b;--card:#2c2535;--border:rgba(190,207,228,.15);--fg:#becfe4;--muted:#948da0;
--accent:#f6847e;--hover:#bd3fd8;--green:#2ea043;--grey:#948da0}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent);text-decoration:none}a:hover{color:var(--hover);text-decoration:underline}
.wrap{max-width:1100px;margin:0 auto;padding:2rem 1.25rem 4rem}
header h1{margin:0 0 .25rem;font-size:1.9rem}
header p{color:var(--muted);margin:.25rem 0}
.repo{display:inline-block;margin-top:.5rem;padding:.4rem .8rem;border:1px solid var(--border);
border-radius:6px;background:var(--card)}
.note{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--accent);
border-radius:6px;padding:.75rem 1rem;margin:1.5rem 0;color:var(--muted);font-size:.92rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:1rem;margin-top:1rem}
.card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.1rem;
display:flex;flex-direction:column}
.card.unreleased{opacity:.72}
.card h2{margin:0 0 .4rem;font-size:1.2rem}
.meta{color:var(--muted);font-size:.85rem;margin:.1rem 0}
.desc{font-size:.92rem;margin:.6rem 0 .8rem}
.badges{margin:.2rem 0 .4rem}
.badge{display:inline-block;font-size:.72rem;padding:.12rem .5rem;border-radius:20px;
margin:0 .3rem .3rem 0;border:1px solid var(--border);color:var(--muted)}
.badge.gt{border-color:var(--green);color:var(--green)}
.badge.warn{border-color:#d29922;color:#d29922}
.files{margin-top:auto;display:flex;flex-wrap:wrap;gap:.4rem;padding-top:.6rem}
.dl{display:inline-block;font-size:.82rem;padding:.32rem .6rem;border:1px solid var(--accent);
border-radius:6px;color:var(--accent);background:transparent}
.dl:hover{background:var(--accent);color:#221c2b;text-decoration:none}
.links{margin-top:.6rem;font-size:.85rem}
.cite{margin-top:.6rem;font-size:.85rem}
.cite summary{cursor:pointer;color:var(--accent);list-style:none}
.cite summary:hover{color:var(--hover)}
.cite summary::-webkit-details-marker{display:none}
.cite summary::before{content:"\25B8 ";color:var(--muted)}
.cite[open] summary::before{content:"\25BE "}
.cite pre{background:#2a2333;border:1px solid var(--border);border-radius:6px;
padding:.6rem .7rem;overflow:auto;font-size:.76rem;line-height:1.45;margin:.4rem 0 0;
white-space:pre;color:var(--fg)}
footer{margin-top:3rem;color:var(--muted);font-size:.85rem;text-align:center}
"""


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def card_html(d) -> str:
    badges = []
    if d.pose_gt:
        badges.append('<span class="badge gt">Pose GT</span>')
    if d.image_frames:
        badges.append('<span class="badge gt">Image frames</span>')
    if d.data_format:
        badges.append(f'<span class="badge">{esc(d.data_format)}</span>')
    if d.license:
        badges.append(f'<span class="badge">{esc(d.license)}</span>')
    if not d.released:
        badges.append('<span class="badge warn">data not released</span>')
    badges_html = "".join(badges)

    if d.files:
        buttons = "".join(
            f'<a class="dl" href="{esc(f.url)}" download>{esc(f.display)}</a>'
            for f in d.files
        )
        files_html = f'<div class="files">{buttons}</div>'
    elif not d.released:
        target = d.paper or d.homepage
        files_html = ('<div class="note" style="margin:.6rem 0 0">Data not publicly '
                      'released yet. ' + (f'<a href="{esc(target)}">See paper</a>.'
                      if target else "") + "</div>")
    else:
        target = d.homepage or d.paper
        files_html = ('<div class="note" style="margin:.6rem 0 0">Download links are '
                      'access-controlled. ' + (f'<a href="{esc(target)}">Visit the '
                      'dataset portal</a>.' if target else "") + "</div>")

    links = []
    if d.homepage:
        links.append(f'<a href="{esc(d.homepage)}">Homepage</a>')
    if d.paper:
        links.append(f'<a href="{esc(d.paper)}">Paper</a>')
    links_html = f'<div class="links">{" &middot; ".join(links)}</div>' if links else ""

    cite_html = ""
    if d.citation:
        cite_html = (f'<details class="cite"><summary>Cite</summary>'
                     f'<pre>{esc(d.citation.strip())}</pre></details>')

    meta = []
    if d.modalities:
        meta.append(f'<div class="meta">Sensors: {esc(d.modalities)}</div>')

    cls = "card unreleased" if not d.released else "card"
    return f"""    <div class="{cls}">
      <h2>{esc(d.name)}</h2>
      <div class="meta">{esc(d.category)}</div>
      {''.join(meta)}
      <div class="badges">{badges_html}</div>
      <div class="desc">{esc(d.description)}</div>
      {links_html}
      {files_html}
      {cite_html}
    </div>"""


def build() -> str:
    cards = "\n".join(card_html(d) for d in DATASETS)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Awesome SLAM Dataset Downloaders</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Awesome SLAM Dataset Downloaders</h1>
    <p>Curated SLAM datasets with direct download links.</p>
    <a class="repo" href="{REPO_URL}">&#9733; View on GitHub</a>
  </header>
  <div class="note">
    Download buttons link directly to each dataset's host (Zenodo, SEANOE, Wasabi,
    Seafile, &hellip;); your browser downloads from there. For automatic
    download <em>and extraction</em>, clone the repo and run the local tool:
    <code>python web_downloader.py</code> or <code>python -m source.&lt;name&gt;</code>.
  </div>
  <div class="grid">
{cards}
  </div>
  <footer>
    Generated from <code>source/registry.py</code> by <code>build_site.py</code>.
    &middot; <a href="{REPO_URL}">{REPO_URL}</a>
  </footer>
</div>
</body>
</html>
"""


def manifest() -> str:
    return json.dumps([
        {
            "name": d.name, "category": d.category, "description": d.description,
            "modalities": d.modalities, "data_format": d.data_format,
            "homepage": d.homepage, "paper": d.paper, "citation": d.citation,
            "license": d.license,
            "pose_gt": d.pose_gt, "image_frames": d.image_frames, "released": d.released,
            "files": [{"label": f.display, "url": f.url} for f in d.files],
        }
        for d in DATASETS
    ], indent=2)


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(build(), encoding="utf-8")
    (DOCS / "datasets.json").write_text(manifest(), encoding="utf-8")
    print(f"Wrote {DOCS / 'index.html'} and {DOCS / 'datasets.json'} "
          f"({len(DATASETS)} datasets)")


if __name__ == "__main__":
    main()
