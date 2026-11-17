---
id: computing-software.software-engineering.uv.uv-project-layout-files
name: uv-project-layout-files
category: computing-software
field: software-engineering
product: uv
tags: [uv, pyproject, uv-lock, venv, project-layout, lockfile, pylock, python]
level: practitioner
status: docs-checked
description: "Explain what pyproject.toml, .venv and uv.lock each do in a uv project, what to commit, and how pylock.toml relates to uv.lock."
sources: [https://docs.astral.sh/uv/concepts/projects/layout/, https://docs.astral.sh/uv/concepts/projects/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv project files and environment

Goal: know which file uv reads or writes, which belong in version control, and which to leave alone.

## Method

- `pyproject.toml`: required; uv uses it to identify the project root. Minimal form is a `[project]` table with `name` and `version`. It also carries the Python version requirement, dependencies, build system and entry points.
- `.venv`: the persistent project environment, created next to `pyproject.toml` so editors can find it. Do not commit it; uv excludes it from git with an internal `.gitignore`.
- `uv.lock`: created next to `pyproject.toml`. It is a universal (cross-platform) lockfile covering all Python markers (OS, architecture, Python version) and records exact resolved versions. Commit it. It is human-readable TOML but managed by uv: do not edit by hand, and other tools cannot use the format.
- `uv run` creates the environment if missing or brings it up to date; `uv sync` creates it explicitly. Both create or update `uv.lock`; `uv lock` updates it explicitly.
- Run commands in the environment with `uv run`, or activate it as any virtual environment.
- Temporary environments exist too, for example `uv run --isolated`.

## pylock.toml

PEP 751 `pylock.toml` is a standard, tool-agnostic output format meant to replace `requirements.txt`. uv keeps `uv.lock` for projects because some features cannot be expressed in `pylock.toml`, but supports it as an export target and in `uv pip`:

- Export: `uv export -o pylock.toml`
- From requirements: `uv pip compile requirements.in -o pylock.toml`
- Install: `uv pip sync pylock.toml` or `uv pip install -r pylock.toml`

## Gotchas

- Do not modify the project environment with `uv pip install`. Use `uv add` for project dependencies, and `uvx` or `uv run --with` for one-off requirements.
- To stop uv managing locking and syncing, set in `pyproject.toml`:

```toml
[tool.uv]
managed = false
```

- With the `centralized-project-envs` preview feature, the environment lives in the uv cache and `.venv` becomes a link to it. Explicit paths (`UV_PROJECT_ENVIRONMENT`, `--active`) are not centralized.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/layout; concepts/projects). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
