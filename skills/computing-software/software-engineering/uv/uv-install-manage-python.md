---
id: computing-software.software-engineering.uv.uv-install-manage-python
name: uv-install-manage-python
category: computing-software
field: software-engineering
product: uv
tags: [uv, python-install, managed-python, python-upgrade, python-list, python-executables, python-versions]
level: practitioner
status: docs-checked
description: "Install, list and upgrade uv-managed Python versions, place python executables on PATH, and understand minor version directories."
sources: [https://docs.astral.sh/uv/concepts/python-versions/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install and manage Python with uv

Goal: install, list and upgrade managed Python versions without surprising existing virtual environments.

## Method

Install (versions are also downloaded automatically when needed):

- `uv python install 3.12.3` exact; `uv python install 3.12` latest patch
- `uv python install '>=3.8,<3.10'` constraint; `uv python install 3.9 3.10 3.11` several
- `uv python install pypy` an implementation
- With no argument, uv ensures a managed Python is installed. If `.python-version` exists it installs that version; a `.python-versions` file lists several versions to install.
- Available versions are frozen per uv release: upgrade uv to get newer ones.

Executables: on Unix `uv python install 3.12` adds `python3.12` to `~/.local/bin`. If that is not on PATH, run `uv python update-shell`. The experimental `--default` flag also installs `python` and `python3`. uv overwrites only executables it manages unless you pass `--force`. By default it points each minor-version executable at the latest patch:

```console
$ uv python install 3.12.7  # Adds `python3.12` to `~/.local/bin`
$ uv python install 3.12.6  # Does not update `python3.12`
$ uv python install 3.12.8  # Updates `python3.12` to point to 3.12.8
```

Upgrade (managed versions only; not PyPy, GraalPy or Pyodide). Patch upgrades only, never across minor versions:

```console
$ uv python upgrade 3.12
$ uv python upgrade
```

After an upgrade uv prefers the new version but keeps the old one. Virtual environments on that minor version upgrade automatically, except ones created with an explicit patch such as `uv venv -p 3.10.8`.

Minor version directories implement this: a directory like `cpython-3.12-macos-aarch64-none` under the uv python directory is a symlink (Unix) or junction (Windows) to a patch directory such as `cpython-3.12.11-macos-aarch64-none`. If another tool resolves the link and builds a venv from the real path, that venv will not auto-upgrade.

List: `uv python list`; filter with `uv python list 3.13` or `uv python list pypy`. Defaults hide other platforms and old patches; use `--all-versions`, `--all-platforms`, or `--only-installed`.

## Gotchas

- Windows: managed installs are registered per PEP 514, so `uv python install 3.13.1` then `py -V:Astral/CPython3.13.1` works; uninstall removes the entry.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/python-versions). Removed or changed: removed an invented Verify step.

Method: documentation only; no commands were run.
