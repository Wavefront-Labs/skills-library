---
id: computing-software.software-engineering.typer.typer-build-package
name: typer-build-package
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, packaging, uv, pyproject, pypi, completion]
level: advanced
status: docs-checked
description: "Package a Typer app with uv: project.scripts entry point, uv build wheel, uv tool install, a __main__.py for python -m, PyPI publish, and typer utils docs."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/package.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build and publish a Typer package with uv

Packaging gives users an independent program and is required for shell completion (unless run through the `typer` command). The page uses uv as one opinionated option.

## Steps

1. `uv init --package rick-portal-gun`, then enter the directory. Prefix the name with your own name so it does not collide with a package created by someone else.
2. `uv add typer` creates the virtual environment (`.venv`). Layout: `pyproject.toml`, `README.md`, `src/rick_portal_gun/__init__.py`, `uv.lock`.
3. Create `src/rick_portal_gun/main.py`. No `if __name__ == "__main__":` is needed for an installed package.

```python
import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def shoot():
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")


@app.command()
def load():
    """
    Load the portal gun
    """
    typer.echo("Loading portal gun")
```
4. Register the script in `pyproject.toml`:

```toml
[project.scripts]
rick-portal-gun = "rick_portal_gun.main:app"
```

The left side is the terminal command name; `rick_portal_gun.main` is the module (underscores); `app` is the object imported and called.

5. `uv sync` installs it into the environment; `rick-portal-gun --help` now works.
6. `uv build` writes `dist/rick_portal_gun-0.1.0-py3-none-any.whl` and a `.tar.gz`.
7. `uv tool install path/to/dist/rick_portal_gun-0.1.0-py3-none-any.whl` installs it in an isolated environment. Then `rick-portal-gun --install-completion` sets up global completion (remove it by deleting the added line in the file the command reports).

## python -m support (optional)

Add `__main__.py` beside `main.py` containing `from .main import app` then `app()`. No pyproject entry needed. Call with the importable name: `python -m rick_portal_gun`. TAB completion does not work this way, because completion is tied to the program name.

## Publish

`export UV_PUBLISH_TOKEN=<pypi token>`, then `uv publish`. Install from PyPI with `uv tool install rick-portal-gun` (after `uv tool uninstall rick-portal-gun`).

## Generate docs

`typer rick_portal_gun.main utils docs --output README.md --name rick-portal-gun` prints `Docs saved to: README.md`. Bump `version` in `pyproject.toml`, then `uv build` and `uv publish` to ship it.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/package.md. Removed or trimmed: the generalisation to any shell rc file (the page names the one file the command edited) and the PyPI-specific reason for the name prefix (page says collision with someone else's package).

Method: documentation only; no commands were run.
