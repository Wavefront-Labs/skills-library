---
id: computing-software.software-engineering.uv.uv-script-locking-python
name: uv-script-locking-python
category: computing-software
field: software-engineering
product: uv
tags: [uv, scripts, lockfile, exclude-newer, reproducibility, python-version, gui-scripts]
level: practitioner
status: docs-checked
description: "Lock PEP 723 script dependencies with uv lock --script, pin the resolution date with exclude-newer, choose Python versions and run .pyw GUI scripts."
sources: [https://docs.astral.sh/uv/guides/scripts/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reproducible scripts: locking, dates and Python versions

Goal: make a PEP 723 script resolve to the same dependencies later, and control which Python runs it.

## Method

Lock (scripts are never locked automatically, unlike projects):

```console
$ uv lock --script example.py
```

This writes `example.py.lock` next to the script. After that, `uv run --script`, `uv add --script`, `uv export --script` and `uv tree --script` reuse the locked dependencies and update the lockfile if necessary. With no lockfile, `uv export --script` still works but creates none.

Limit resolution by date: add `exclude-newer` under `[tool.uv]` in the inline metadata, as an RFC 3339 timestamp, e.g. `2006-12-02T02:07:43Z`:

```python
# /// script
# dependencies = [
#   "requests",
# ]
# [tool.uv]
# exclude-newer = "2023-10-16T00:00:00Z"
# ///
```

uv then only considers distributions released before that date.

Python versions:

- Request one per run: `uv run --python 3.10 example.py` (default is whatever uv finds, e.g. 3.12.6).
- Or declare `requires-python = ">=3.12"` in the metadata block; uv searches for or downloads a matching Python.

GUI scripts: on Windows, uv runs a script ending in `.pyw` with `pythonw`:

```console
PS> uv run example.pyw
PS> uv run --with PyQt5 example_pyqt.pyw
```

## Verify

A script that prints `sys.version_info[:3]` shows `3.10.15` under `--python 3.10` in the guide's example. After `uv lock --script example.py`, the file `example.py.lock` exists beside the script.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/scripts). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
