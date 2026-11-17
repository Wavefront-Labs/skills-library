---
id: computing-software.software-engineering.uv.uv-pip-compile-requirements
name: uv-pip-compile-requirements
category: computing-software
field: software-engineering
product: uv
tags: [uv, uv-pip-compile, requirements-in, pip-constraints, pip-sync, overrides, build-constraints]
level: practitioner
status: docs-checked
description: "Declare dependencies in pyproject.toml or requirements.in, lock them with uv pip compile, upgrade pins, sync with uv pip sync, and use constraints and overrides."
sources: [https://docs.astral.sh/uv/pip/dependencies/, https://docs.astral.sh/uv/pip/compile/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declaring and locking requirements with uv pip

Goal: turn declared dependencies into an exactly pinned `requirements.txt` and sync an environment to it.

## Method

Declare in `[project] dependencies` and `[project.optional-dependencies]` (each key is an extra) in pyproject.toml, or one requirement per line in `requirements.in` (no extras or groups there).

Compile (by default the output is displayed; `-o`/`--output-file` writes it to a file):

- `uv pip compile pyproject.toml -o requirements.txt`
- `uv pip compile requirements.in -o requirements.txt`
- several inputs: `uv pip compile pyproject.toml requirements-dev.in -o requirements-dev.txt`
- legacy: `uv pip compile setup.py -o requirements.txt` (setup.cfg also works)
- stdin: `echo "ruff" | uv pip compile -`
- extras: `--extra foo` or `--all-extras` (extras are not supported with the `requirements.in` format)
- groups: `uv pip compile --group foo`, `--project some/path/ --group foo`, or `--group some/path/pyproject.toml:foo`. A `--group` does not apply to other named sources.

Upgrades: with an output file, existing pins are kept. Use `--upgrade-package ruff` for one package or `--upgrade` for all.

Sync: `uv pip install -r requirements.txt` leaves undeclared packages in place. `uv pip sync requirements.txt` makes the environment exactly match; it also accepts a PEP 751 `pylock.toml`.

Constraints (limit versions, never trigger installs): `uv pip compile requirements.in --constraint constraints.txt` with lines like `pydantic<2.0`. `constraint-dependencies` in the workspace-root pyproject.toml are appended.

Build constraints: `--build-constraint build-constraints.txt` (e.g. `setuptools==75.0.0`), plus `build-constraint-dependencies` from the workspace root. For hashes put `--hash=sha256:...` on the line and add `--require-build-hashes`. For runtime dependencies use `--require-hashes` with `uv pip install` or `uv pip sync`.

Overrides replace a package's requirements absolutely (constraints are additive): `uv pip compile requirements.in --override overrides.txt` with `c>=2.0` resolves a clash where `a` needs `c<2.0` and `b` needs `c>=2.0`. If `a` was right, expect runtime errors.

## Verify

`echo "ruff==0.3.0" > requirements.txt` then `echo "ruff" | uv pip compile - -o requirements.txt` outputs `ruff==0.3.0`, pin retained.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (pip/dependencies; pip/compile). Removed or changed: reworded "output goes to stdout" to the page wording (output is displayed) and replaced an overbroad "pyproject only" note on extras with the page statement that extras are not supported in requirements.in.

Method: documentation only; no commands were run.
