---
id: computing-software.software-engineering.uv.uv-migrate-pip-to-project
name: uv-migrate-pip-to-project
category: computing-software
field: software-engineering
product: uv
tags: [uv, migration, requirements-txt, pip-tools, uv-add, dependency-groups, lockfile]
level: practitioner
status: docs-checked
description: "Migrate a pip or pip-tools requirements.txt workflow to a uv project: import requirements with uv add, keep locked versions, handle platforms and dev groups."
sources: [https://docs.astral.sh/uv/guides/migration/pip-to-project/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating requirements files to a uv project

Goal: replace `requirements.in`/`requirements.txt` with `pyproject.toml` and `uv.lock` without changing locked versions.

## Method

Mapping: `requirements.in` becomes `[project] dependencies` (groups go in `[dependency-groups]`, e.g. `dev = ["pytest"]`); `requirements.txt` becomes `uv.lock`. The lockfile is always universal, so one file covers all platforms and all groups. Use `tool.uv.environments` to lock for fewer platforms.

1. `uv init` to create a pyproject.toml.
2. Import with `uv add -r requirements.in`. That re-solves, so keep the old pins by also passing the compiled file as constraints: `uv add -r requirements.in -c requirements.txt`.
3. Platform-specific compiled files cannot be passed to `-c` as they are, because they lack markers and will conflict. Add markers first, per platform:

```console
$ uv pip compile requirements.in -o requirements-win.txt --python-platform windows --no-strip-markers
```

Repeat with `linux` and `macos` and matching `-o` files (uv constrains to the existing output file where it can). Then:

```console
$ uv add -r requirements.in -c requirements-win.txt -c requirements-linux.txt
```

4. Development dependencies: `uv add --dev -r requirements-dev.in -c requirements-dev.txt`. If the dev file includes `-r requirements.in`, strip that line so the base requirements do not enter the dev group: `sed '/^-r /d' requirements-dev.in | uv add --dev -r - -c requirements-dev.txt`.
5. Other groups: `uv add -r requirements-docs.in -c requirements-docs.txt --group docs`.
6. Path and Git requirements (`./path-dep`, `-e ./editable-path-dep`, `git-dep @ git+https://...`) become entries in `[tool.uv.sources]`, with `editable = true` for `-e`.
7. Run with `uv run pytest`. uv uses the project `.venv` and ignores the active environment (`VIRTUAL_ENV`) unless `--active` is passed. `uv sync` creates the environment explicitly, for editors.

If you still need one universal requirements file, `uv pip compile --universal requirements.in` emits markers such as `colorama==0.4.6 ; sys_platform == 'win32'`.

## Gotchas

- The page notes the guides for migrating to the drop-in `uv pip` interface, or from an existing pyproject.toml workflow, were not yet written.

## Verify

Per the page, after `uv add -r requirements.in -c requirements.txt` the existing versions are retained when `uv.lock` is produced; `uv lock` creates the lockfile explicitly.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/migration/pip-to-project). Removed or changed: reworded Verify to the page statement (uv lock creates the lockfile; existing versions are retained).

Method: documentation only; no commands were run.
