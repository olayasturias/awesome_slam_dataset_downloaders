import importlib
from pathlib import Path
from flask import Flask, render_template_string, request, redirect, url_for, flash, jsonify
import webview
import threading
import time

app = Flask(__name__)
app.secret_key = 'slam_secret_key'

# List of available downloaders
DOWNLOADERS = [
    {
        'name': 'SubPipe',
        'module': 'source.subpipe',
        'function': 'download_subpipe',
        'param': 'output_folder',
    },
    {
        'name': 'SOTRUE',
        'module': 'source.sotrue',
        'function': 'download_and_extract_tar_files',
        'param': 'output_directory',
    },
    {
        'name': 'EiffelTower',
        'module': 'source.eiffel_tower',
        'function': 'download_eiffel_tower',
        'param': 'output_folder',
    },
    {
        'name': 'Aqualoc Archaeological Site',
        'module': 'source.aqualoc',
        'function': 'download_aqualoc_archaeological_site_sequences',
        'param': 'output_folder',
    },
    {
        'name': 'Aqualoc Harbor Site',
        'module': 'source.aqualoc',
        'function': 'download_aqualoc_harbor_site_sequences',
        'param': 'output_folder',
    },
]

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
          {% for d in downloaders %}
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="downloader" value="{{ loop.index0 }}" id="downloader_{{ loop.index0 }}">
              <label class="form-check-label" for="downloader_{{ loop.index0 }}">{{ d.name }}</label>
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
// pywebview integration for folder picker
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

# Global dict to track progress and control
progress_status = {}
stop_flags = {}

# Helper to wrap downloaders for progress
class DownloadThread(threading.Thread):
    def __init__(self, idx, func, param):
        super().__init__()
        self.idx = idx
        self.func = func
        self.param = param
        self.daemon = True
    def run(self):
        progress_status[self.idx] = {'progress': 0, 'status': 'Downloading'}
        try:
            # Simulate progress for demo; replace with real progress reporting
            for i in range(1, 101):
                if stop_flags.get(self.idx):
                    progress_status[self.idx] = {'progress': i, 'status': 'Stopped'}
                    return
                progress_status[self.idx] = {'progress': i, 'status': 'Downloading'}
                time.sleep(0.05)  # Simulate work
            self.func(self.param)
            progress_status[self.idx] = {'progress': 100, 'status': 'Completed'}
        except Exception as e:
            progress_status[self.idx] = {'progress': 0, 'status': f'Error: {e}'}

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
            downloader = DOWNLOADERS[int(idx)]
            try:
                mod = importlib.import_module(downloader['module'])
                func = getattr(mod, downloader['function'])
                param = folder
                if 'Path' in str(func.__annotations__.get(downloader['param'], '')):
                    param = Path(folder)
                # Start download in background thread
                stop_flags[int(idx)] = False
                thread = DownloadThread(int(idx), func, param)
                thread.start()
                messages.append(f"Download started for {downloader['name']} in {folder}")
            except Exception as e:
                messages.append(f"Error for {downloader['name']}: {e}")
        for msg in messages:
            flash(msg)
        return redirect(url_for('index'))
    return render_template_string(HTML, downloaders=DOWNLOADERS, default_folder=default_folder, progress_status=progress_status)

def run_app():
    window = webview.create_window('SLAM Dataset Downloader', app, js_api=Api())
    webview.start()

if __name__ == '__main__':
    run_app()
