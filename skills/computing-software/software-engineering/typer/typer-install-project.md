---
id: computing-software.software-engineering.typer.typer-install-project
name: typer-install-project
category: computing-software
field: software-engineering
product: typer
tags: [typer, install, uv, virtual-environment, completion, pip]
level: intro
status: docs-checked
description: "Set up a project with uv init --bare and uv add typer, activate .venv for the typer command, install shell completion, and add the bundled AI agent skill."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/install.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install Typer in a uv project

## Create the project and add Typer

Install `uv` first, then:

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add typer
```

- `uv init`: new Python project; `--bare` creates only a minimal `pyproject.toml` (no sample `main.py`, `README.md` etc.).
- `uv add` creates the virtual environment in `.venv`, adds Typer to `pyproject.toml` and writes `uv.lock`, recording exact versions so the same packages can be installed later on another computer or when distributing the app (called locking).
- `uv` uses a compatible Python already installed, or downloads one.
- `typer` by default comes with `rich` and `shellingham`.

Run project commands with `uv run`, e.g. `uv run python main.py`.

## Activate the environment for the typer command

`uv add typer` installs the library and the `typer` command in `.venv`. To use `typer` directly (needed to set up its shell completion), activate:

```console
$ source .venv/bin/activate         # Linux, macOS
$ .venv\Scripts\Activate.ps1        # Windows PowerShell
$ source .venv/Scripts/activate     # Windows Bash
$ typer --install-completion
```

Restart the terminal for completion to take effect. Activate the environment again in every new terminal session where you want `typer` directly.

## Without uv

Create and activate a virtual environment yourself and run `pip install typer`.

## AI agent skill

Typer ships an official skill for AI coding agents inside the package, so it matches the installed version and updates with Typer. After installing Typer, run:

```console
$ uvx library-skills
```

`uvx` is an alias for `uv tool run`; it runs Library Skills in a temporary isolated environment that scans packages installed in your project. For Claude Code, choose `.claude/skills` when asked where to install it.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/install.md. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
