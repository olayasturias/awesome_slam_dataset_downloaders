import logging
import threading
from pathlib import Path

import webview
from flask import Flask, render_template_string, request, redirect, url_for, flash, jsonify

from source.registry import DATASETS

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = Flask(__name__)
app.secret_key = 'slam_secret_key'

HTML = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SLAM Dataset Downloader</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.2/dist/vapor/bootstrap.min.css">
</head>
<body>
<div class="container mt-5">
  <div class="card shadow-lg">
    <div class="card-body">
      <h2 class="card-title mb-4">Select the Awesome Dataset to Download</h2>
      <form method=post id="downloaderForm">
        <div class="mb-3">
          <label class="form-label">Datasets:</label><br>
          {% for d in datasets %}
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="downloader" value="{{ loop.index0 }}" id="downloader_{{ loop.index0 }}" {% if not d.released %}disabled{% endif %}>
              <label class="form-check-label" for="downloader_{{ loop.index0 }}">
                {{ d.name }}
                <small class="text-muted">&mdash; {{ d.category }}{% if d.data_format %}, {{ d.data_format }}{% endif %}</small>
                {% if not d.released %}<span class="badge bg-secondary">data not released</span>{% endif %}
              </label>
            </div>
          {% endfor %}
        </div>
        <div class="mb-3">
          <label for="folder" class="form-label">Download Folder:</label>
          <div class="input-group">
            <input type="text" class="form-control" name="folder" id="folder" value="{{ default_folder }}" size="50">
            <button type="button" class="btn btn-secondary" onclick="window.pywebview.api.select_folder().then(function(folder){if(folder){document.getElementById('folder').value=folder;}})">Select Folder</button>
          </div>
        </div>
        <button type="submit" class="btn btn-primary">Download</button>
      </form>
      {% with messages = get_flashed_messages() %}
        {% if messages %}
          <div class="alert alert-info mt-4">
            <ul class="mb-0">
            {% for message in messages %}
              <li>{{ message }}</li>
            {% endfor %}
            </ul>
          </div>
        {% endif %}
      {% endwith %}
      <div class="mt-4">
        <h4>Download Progress</h4>
        <div id="progressStatus">
          {% for idx, status in progress_status.items() %}
            <div class="progress mb-2" data-idx="{{ idx }}">
              <div class="progress-bar" role="progressbar" style="width: {{ status.progress }}%;" aria-valuenow="{{ status.progress }}" aria-valuemin="0" aria-valuemax="100">{{ status.progress }}% - {{ status.status }}</div>
            </div>
          {% endfor %}
        </div>
      </div>
    </div>
  </div>
</div>
<script>
function updateProgress() {
  {% for idx, status in progress_status.items() %}
    fetch('/progress/{{ idx }}')
      .then(response => response.json())
      .then(data => {
        const progressBar = document.querySelector('.progress[data-idx="{{ idx }}"] .progress-bar');
        if (progressBar) {
          progressBar.style.width = data.progress + '%';
          progressBar.setAttribute('aria-valuenow', data.progress);
          progressBar.innerText = data.progress + '% - ' + data.status;
        }
      });
  {% endfor %}
}
setInterval(updateProgress, 1000);
</script>
</body>
</html>
'''

# Global dicts to track progress and control
progress_status = {}
stop_flags = {}


class DownloadThread(threading.Thread):
    """Run a dataset download in the background, reporting real progress."""

    def __init__(self, idx, dataset, folder):
        super().__init__()
        self.idx = idx
        self.dataset = dataset
        self.folder = folder
        self.daemon = True

    def run(self):
        progress_status[self.idx] = {'progress': 0, 'status': 'Downloading'}

        def progress_cb(fraction, message):
            if stop_flags.get(self.idx):
                # Cooperative stop: raised inside the worker to unwind the download.
                raise RuntimeError("stopped")
            progress_status[self.idx] = {
                'progress': int(fraction * 100),
                'status': message,
            }

        try:
            self.dataset.download(self.folder, progress_cb=progress_cb)
            progress_status[self.idx] = {'progress': 100, 'status': 'Completed'}
        except RuntimeError as exc:
            if str(exc) == "stopped":
                progress_status[self.idx] = {
                    'progress': progress_status[self.idx]['progress'], 'status': 'Stopped'}
            else:
                progress_status[self.idx] = {'progress': 0, 'status': f'Error: {exc}'}
        except Exception as exc:  # noqa: BLE001 - surface any error in the UI
            progress_status[self.idx] = {'progress': 0, 'status': f'Error: {exc}'}


@app.route('/progress/<int:idx>')
def progress(idx):
    return jsonify(progress_status.get(idx, {'progress': 0, 'status': 'Idle'}))


@app.route('/stop/<int:idx>', methods=['POST'])
def stop(idx):
    stop_flags[idx] = True
    return jsonify({'stopped': True})


class Api:
    def select_folder(self):
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        folder = filedialog.askdirectory()
        root.destroy()
        return folder


@app.route('/', methods=['GET', 'POST'])
def index():
    default_folder = str(Path.home() / 'Downloads')
    if request.method == 'POST':
        idxs = request.form.getlist('downloader')
        folder = request.form['folder']
        messages = []
        for idx in idxs:
            i = int(idx)
            dataset = DATASETS[i]
            if not dataset.released:
                messages.append(f"{dataset.name}: data not released yet, skipped.")
                continue
            stop_flags[i] = False
            DownloadThread(i, dataset, folder).start()
            messages.append(f"Download started for {dataset.name} in {folder}")
        for msg in messages:
            flash(msg)
        return redirect(url_for('index'))
    return render_template_string(HTML, datasets=DATASETS, default_folder=default_folder,
                                  progress_status=progress_status)


def run_app():
    webview.create_window('SLAM Dataset Downloader', app, js_api=Api())
    webview.start()


if __name__ == '__main__':
    run_app()
