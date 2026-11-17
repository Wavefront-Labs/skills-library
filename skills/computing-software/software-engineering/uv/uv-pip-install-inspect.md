---
id: computing-software.software-engineering.uv.uv-pip-install-inspect
name: uv-pip-install-inspect
category: computing-software
field: software-engineering
product: uv
tags: [uv, uv-pip-install, pip-packages, pip-inspection, pip-list, pip-freeze, pip-check]
level: practitioner
status: docs-checked
description: "Install, uninstall and inspect packages with uv pip: specifiers, git and editable installs, requirements and pyproject inputs, groups, list, freeze, show, check."
sources: [https://docs.astral.sh/uv/pip/packages/, https://docs.astral.sh/uv/pip/inspection/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv pip: manage and inspect packages

Goal: install into and inspect the current virtual environment with pip-style commands.

## Method

Install:

- `uv pip install flask`; extras `uv pip install "flask[dotenv]"`; several `uv pip install flask ruff`.
- Constraints: `uv pip install 'ruff>=0.2.0'`, `'ruff==0.3.0'`.
- Disk: `uv pip install "ruff @ ./projects/ruff"`.
- Git: `uv pip install "git+https://github.com/astral-sh/ruff"`, with a tag `@v0.2.0`, a commit hash, or a branch `@main`. Private repositories are covered by the Git authentication docs.
- Editable (source changes apply without reinstall): `uv pip install -e .` or `uv pip install -e "ruff @ ./project/ruff"`.

Install from files:

- `uv pip install -r requirements.txt`
- `uv pip install -r pyproject.toml`, with `--extra foo` or `--all-extras`
- Dependency groups: `uv pip install --group foo` (from `./pyproject.toml`); `--project some/path/ --group foo --group bar`; or a path per group, `--group some/path/pyproject.toml:foo`.

Uninstall: `uv pip uninstall flask` or `uv pip uninstall flask ruff`.

Inspect:

- `uv pip list`, and `uv pip list --format json`
- `uv pip freeze` lists packages in requirements.txt format
- `uv pip show numpy` (several packages at once are allowed)
- `uv pip check` reports conflicts or missing dependencies

## Gotchas

- `--group` flags do not apply to other sources given with `-r` or `-e`: `uv pip install -r some/path/pyproject.toml --group foo` takes `foo` from `./pyproject.toml`, not `some/path/pyproject.toml`.
- Conflicting requirements can end up in one environment if installed in multiple steps; that is what `uv pip check` finds.

## Verify

`uv pip check` after installs reports conflicts or missing dependencies if any; `uv pip list` shows the installed packages.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (pip/packages; pip/inspection). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
