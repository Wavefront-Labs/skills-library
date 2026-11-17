---
id: computing-software.software-engineering.uv.uv-python-discovery
name: uv-python-discovery
category: computing-software
field: software-engineering
product: uv
tags: [uv, python-discovery, managed-python, python-preference, python-downloads, system-python, python-versions]
level: practitioner
status: docs-checked
description: "How uv discovers Python interpreters and how to control automatic downloads and the managed versus system preference."
sources: [https://docs.astral.sh/uv/concepts/python-versions/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv Python discovery and preferences

Goal: predict which interpreter uv picks and force managed-only, system-only or no-download behavior.

## Method

Terms: Python versions uv installs are managed; all others (including OS packages and pyenv installs) are system.

Discovery checks, for the request:

- Managed installations in `UV_PYTHON_INSTALL_DIR`.
- `python`, `python3` or `python3.x` on PATH (macOS, Linux), or `python.exe` (Windows).
- Windows: the registry and Microsoft Store interpreters matching the request (see `py --list-paths`).
- Where allowed, a virtual environment's interpreter is checked first.

Non-executable files are ignored; each candidate is queried and skipped if the query fails; the first one satisfying the request is used. Managed searches prefer newer versions first; system searches take the first compatible, not the newest. If nothing is found, uv checks for a compatible managed download.

Control:

- Downloads: `python-downloads` setting, default `automatic`; `manual` allows downloads only in `uv python install`. Set it in a persistent config file, or pass `--no-python-downloads` to any command.
- Managed only: `--managed-python` (e.g. `uv python list --managed-python`). System only: `--no-managed-python`.
- `python-preference` setting: `managed` (default; prefers managed over system, but system is still preferred over downloading), `only-managed`, `system`, `only-system`. `only-managed` equals `--managed-python`, `only-system` equals `--no-managed-python`. Downloads can be disabled without changing the preference.

Pre-releases are not selected by default but are used when nothing else matches (or when you give the path to a pre-release executable); if a matching pre-release exists, uv will not download a stable version instead.

## Gotchas

- CPython builds come from Astral's `python-build-standalone`; the distributions are portable and have some documented quirks.
- PyPy lags CPython and supports versions up to 3.11 (per the page).

## Verify

The page's examples are `uv python list --managed-python` (ignore system Python versions) and `uv python list --no-managed-python` (ignore managed ones); compare their output.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/python-versions). Removed or changed: reworded Verify, which claimed output the page does not show, to the page examples of --managed-python and --no-managed-python.

Method: documentation only; no commands were run.
