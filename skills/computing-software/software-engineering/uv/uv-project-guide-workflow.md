---
id: computing-software.software-engineering.uv.uv-project-guide-workflow
name: uv-project-guide-workflow
category: computing-software
field: software-engineering
product: uv
tags: [uv, project-workflow, lockfile, uv-init, uv-add, uv-run, uv-build, projects-guide]
level: practitioner
status: docs-checked
description: "Work a uv project end to end: uv init, generated files, uv add and remove, lock upgrades, uv version, uv run versus activation, and uv build."
sources: [https://docs.astral.sh/uv/guides/projects/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv project workflow, init to run

Goal: create a project and take it through dependencies, versioning, running and building.

## Method

1. Create: `uv init hello-world` (or `uv init` in the current directory). It makes `.git/`, `.gitignore`, `.python-version`, `pyproject.toml`, `README.md` and `src/hello_world/__init__.py`. The pyproject defines a `hello-world` entry point under `[project.scripts]` and a `[build-system]` using `uv_build`. `uv run hello-world` prints `Hello from hello-world!`.
2. The first project command (`uv run`, `uv sync` or `uv lock`) creates `.venv/` and `uv.lock`. `.python-version` is the default Python for the environment. `uv.lock` is a cross-platform lockfile of exact versions; commit it and do not edit it by hand. Uv settings go in a `[tool.uv]` section of pyproject.toml.
3. Dependencies: `uv add requests` updates pyproject, lockfile and environment. Also `uv add 'requests==2.31.0'`, `uv add git+https://github.com/psf/requests`, `uv add -r requirements.txt -c constraints.txt` (migrating), `uv remove requests`.
4. Upgrade one package: `uv lock --upgrade-package requests`, which keeps the rest of the lockfile intact.
5. Version: `uv version`; `uv version --short`; `uv version --output-format json` (fields package_name, version, commit_info).
6. Run: `uv run -- flask run -p 3000` or `uv run example.py`. Before each run uv checks the lockfile against pyproject and the environment against the lockfile. By default `uv run` does not remove extraneous packages.
7. Alternative: `uv sync`, then activate (`source .venv/bin/activate` on macOS and Linux, `.venv\Scripts\activate` on Windows) and run commands directly; the environment must be active.
8. Build: `uv build` writes a wheel and an sdist to `dist/`, e.g. `hello_world-0.1.0-py3-none-any.whl` and `hello_world-0.1.0.tar.gz`.

## Verify

`uv run hello-world` prints `Hello from hello-world!`; after `uv build`, `ls dist/` lists the `.whl` and `.tar.gz`.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/projects). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
