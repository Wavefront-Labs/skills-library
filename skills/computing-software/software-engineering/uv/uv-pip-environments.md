---
id: computing-software.software-engineering.uv.uv-pip-environments
name: uv-pip-environments
category: computing-software
field: software-engineering
product: uv
tags: [uv, uv-venv, uv-pip, pip-environments, virtual-environments, system-python, virtual-env]
level: practitioner
status: docs-checked
description: "Create virtual environments with uv venv and control which environment uv pip targets: discovery order, VIRTUAL_ENV, --python and --system."
sources: [https://docs.astral.sh/uv/pip/environments/, https://docs.astral.sh/uv/pip/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environments for the uv pip interface

Goal: create a virtual environment and make `uv pip` commands hit the right Python environment. The pip interface works directly on environments (unlike uv's project commands) and uv does not invoke pip.

## Method

Create: `uv venv` (makes `.venv`), `uv venv my-name`, `uv venv --python 3.11` (uv downloads that Python if it is unavailable). uv requires a virtual environment by default, unlike pip.

Use: with the default `.venv` name, later commands such as `uv pip install ruff` find it automatically. Activation is optional: `source .venv/bin/activate` (macOS and Linux; `activate.fish`, `activate.csh` for other shells), `.venv\Scripts\activate` on Windows. Leave with `deactivate`.

Discovery order for commands that mutate an environment (`uv pip install`, `uv pip sync`):

1. Activated environment from `VIRTUAL_ENV`.
2. Activated Conda environment from `CONDA_PREFIX`.
3. `.venv` in the current directory or the nearest parent.

If none is found, uv prompts you to create one with `uv venv`. Non-mutating commands such as `uv pip compile` need no virtual environment but still need a Python interpreter.

Other targets:

- `VIRTUAL_ENV=/path/to/venv` installs there regardless of where uv lives; it is ignored if the directory is not a PEP 405 virtual environment.
- `uv pip install --python /path/to/python` installs into that interpreter's environment, virtual or not; `--python` also takes a virtual environment root directory.
- `uv pip install --system` targets the system Python, roughly `--python $(which python)` but skipping executables linked to virtual environments. It is appropriate in CI and containers.

## Gotchas

- Interpreters found via `--python 3.12` that are not in virtual environments are ignored unless `--system` is given; with `--system`, interpreters in virtual environments are ignored.
- System installs are not supported everywhere, for example Debian before Python 3.10 (distutils patching); use virtual environments there.
- `python -m uv` defaults to the parent interpreter's environment and adds startup overhead; not recommended generally.

## Verify

After `uv venv` then `uv pip install ruff`, the package installs into `.venv` with no activation needed.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (pip/environments; pip). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
