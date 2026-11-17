---
id: computing-software.software-engineering.uv.uv-first-steps-overview
name: uv-first-steps-overview
category: computing-software
field: software-engineering
product: uv
tags: [uv, first-steps, quickstart, features, overview, commands, pip-interface]
level: intro
status: docs-checked
description: "Confirm uv is installed and map its command groups: Python versions, scripts, projects, tools, the pip interface and utility commands."
sources: [https://docs.astral.sh/uv/getting-started/first-steps/, https://docs.astral.sh/uv/getting-started/features/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv first steps and feature map

Goal: confirm the install works and know which uv command group fits a task. The groups are usable independently or together.

## Method

Run `uv` with no arguments. It prints "An extremely fast Python package manager." followed by usage and the command list.

Pick the group:

- Python versions: `uv python install`, `list`, `find`, `pin` (pin the project to a version), `uninstall`.
- Scripts (standalone files such as `example.py`): `uv run`, `uv add --script`, `uv remove --script`.
- Projects (with a `pyproject.toml`): `uv init`, `add`, `remove`, `sync`, `lock`, `run`, `tree`, `build`, `publish`.
- Tools (such as ruff or black): `uvx` or `uv tool run` for a temporary environment; `uv tool install`, `uninstall`, `list`; `uv tool update-shell` to put tool executables on the shell path.
- pip interface (legacy workflows, or when more control is needed):
  - `uv venv` replaces venv and virtualenv.
  - `uv pip install`, `show`, `freeze`, `check`, `list`, `uninstall`, `tree` replace pip and pipdeptree.
  - `uv pip compile` and `uv pip sync` replace pip-tools.
- Utility: `uv cache clean`, `uv cache prune` (removes outdated entries and all centralized project environments), `uv cache dir`, `uv tool dir`, `uv python dir`, `uv self update`.

## Gotchas

- The pip-interface commands do not exactly match the behaviour of pip, venv or pip-tools. The further from common workflows, the more differences you will meet; consult the pip-compatibility page.

## Verify

`uv` prints the help menu with the available commands.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (getting-started/first-steps; getting-started/features). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
