---
id: computing-software.software-engineering.uv.uv-jupyter-marimo
name: uv-jupyter-marimo
category: computing-software
field: software-engineering
product: uv
tags: [uv, jupyter, notebooks, marimo, ipykernel, uvx, inline-script-metadata, vs-code]
level: practitioner
status: docs-checked
description: "Run Jupyter and marimo notebooks with uv in projects, standalone, or sandboxed, including project kernels and where notebook installs end up."
sources: [https://docs.astral.sh/uv/guides/integration/jupyter/, https://docs.astral.sh/uv/guides/integration/marimo/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jupyter and marimo with uv

Goal: notebooks that see the project environment, and know where packages installed in a notebook land.

## Method

### Jupyter in a project

```console
$ uv run --with jupyter jupyter lab
```

Serves at `http://localhost:8888/lab` by default and can import the project's modules (read-only use needs nothing more).

To install from inside the notebook, create a project kernel:

```console
$ uv add --dev ipykernel
$ uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=project
$ uv run --with jupyter jupyter lab
```

Select the `project` kernel; then `!uv add pydantic` updates the project, while `!uv pip install pydantic` installs into the project venv without touching `pyproject.toml` or `uv.lock`.

Without a kernel: `!uv add` still modifies the project environment, but `!uv pip install` goes into Jupyter's own environment and may vanish on later runs. For `%pip`, run `uv venv --seed` before starting the server; those installs reach the project venv but are not recorded in the project files.

Standalone: `uv tool run jupyter lab` (isolated environment).

Non-project venv: `uv venv --seed`, `uv pip install jupyterlab`, then run `.venv/bin/jupyter lab` (Windows: `.venv\Scripts\jupyter lab`).

VS Code: `uv init project`, `cd project`, `uv add --dev ipykernel`, `code .`; pick the "Python Environments" kernel for `.venv/bin/python`. ipykernel must be in the project environment (`uv pip install ipykernel` also works). To manipulate the environment from the notebook you may need `uv add --dev uv`.

### marimo

- Standalone: `uvx marimo edit` or `uvx marimo edit my_notebook.py`.
- Inline script metadata: `uv add --script my_notebook.py numpy`, then `uvx marimo edit --sandbox my_notebook.py`. marimo uses uv for an isolated environment and records packages installed from its UI in the script metadata.
- In a project with marimo as a dependency: `uv run marimo edit my_notebook.py`; the marimo UI installer invokes `uv add`.
- Project without marimo as a dependency: `uv run --with marimo marimo edit my_notebook.py`. Packages installed in the UI are not added to the project and may disappear.
- Non-project: `uv venv`, `uv pip install marimo`, `uv run marimo edit`.
- Run any marimo notebook as a script without a browser session: `uv run my_notebook.py`.

## Gotchas

`!uv pip install` in a kernel-less Jupyter targets Jupyter's environment, not the project.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/integration/jupyter; guides/integration/marimo). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
