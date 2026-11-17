---
id: computing-software.ai-ml-engineering.open-webui.python-install
name: python-install
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [python-install, pip, uv, venv, conda, data-dir]
level: practitioner
status: docs-checked
description: "Install and run Open WebUI from PyPI with pip, venv, conda or uvx, keep data in DATA_DIR, avoid logouts, and upgrade safely."
sources:
  - https://docs.openwebui.com/getting-started/quick-start/tab-python/Pip
  - https://docs.openwebui.com/getting-started/quick-start/tab-python/Uv
  - https://docs.openwebui.com/getting-started/quick-start/tab-python/Venv
  - https://docs.openwebui.com/getting-started/quick-start/tab-python/Conda
  - https://docs.openwebui.com/getting-started/quick-start/tab-python/PythonUpdating
  - https://docs.openwebui.com/getting-started/quick-start/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run Open WebUI without Docker.

## Python version
Python 3.11 and 3.12 are supported; 3.13 is not yet (installs fail or break at runtime). Production: use Docker or the latest 3.12.

## Install and run
```bash
pip install open-webui
open-webui serve
```
UI at http://localhost:8080. Use `--host` and `--port` (for example `open-webui serve --port 3000`). Set the data location with `DATA_DIR=~/.open-webui open-webui serve`.

Isolated environments:
- venv: `python3 -m venv venv`, `source venv/bin/activate` (Windows: `venv\Scripts\activate`), `pip install open-webui`, `open-webui serve`.
- conda: `conda create -n open-webui python=3.12`, `conda activate open-webui`, `pip install open-webui`, `open-webui serve`.
- uv: install uv (`curl -LsSf https://astral.sh/uv/install.sh | sh`), then `DATA_DIR=~/.open-webui uvx --python 3.12 open-webui@latest serve`. Always set `DATA_DIR` with uvx or data may land in a cache that gets cleared.

## No NVIDIA GPU (Linux x86_64)
The PyPI install pulls the default PyTorch with CUDA libraries. Install first, in the same environment: `pip install torch --index-url https://download.pytorch.org/whl/cpu` (with uv: `uv pip install ...`). For AMD install the ROCm build instead.

## Sessions
The command writes a signing key to `.webui_secret_key` in the directory you start from. Set `WEBUI_SECRET_KEY` or always start from the same directory; a new key signs everyone out.

## Upgrade
`pip install -U open-webui`, then `open-webui serve`. If `UVICORN_WORKERS` is above 1, start the new version once with `UVICORN_WORKERS=1` until migrations finish, then restart (migrations run in every process); scale with replicas instead of workers.

## Gotchas
- `open-webui: command not found`: activate the environment you installed into (`bin`, or `Scripts` on Windows).
- PyPI carries releases only; for unreleased fixes run the Docker `:dev` image with its own volume. Installing from a source checkout or Git URL needs Node.js and npm for the frontend build.
- Without `DATA_DIR` the data sits in `site-packages/open_webui/data` inside the environment; removing the env deletes it, while `pip uninstall` leaves it behind.
- Uninstall: `pip uninstall open-webui`, `conda remove --name open-webui --all`, or `uv tool uninstall open-webui` plus `uv cache clean`.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: the Pip, Uv, Venv, Conda and Python-updating install pages and the quick-start Python compatibility notes. Added the quick-start page to sources. Removed: nothing else.
Method: documentation only; no commands were run.
