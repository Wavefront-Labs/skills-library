---
id: computing-software.software-engineering.uv.uv-python-version-requests
name: uv-python-version-requests
category: computing-software
field: software-engineering
product: uv
tags: [uv, python-versions, python-version-file, python-pin, requires-python, version-request, python-discovery]
level: practitioner
status: docs-checked
description: "Request a Python version in uv with --python, .python-version files, uv python pin and requires-python, using the supported request formats."
sources: [https://docs.astral.sh/uv/concepts/python-versions/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv Python version requests

Goal: tell uv which interpreter to use, per command, per directory or per project.

## Method

Per command: `uv venv --python 3.11.6` (most commands accept `--python`). uv downloads the version if it is not found.

Supported request formats:

- `<version>`: `3`, `3.12`, `3.12.3`
- `<version-specifier>`: `>=3.12,<3.13`
- `<version><short-variant>`: `3.13t`, `3.12.0d`
- `<version>+<variant>`: `3.13+freethreaded`, `3.12.0+debug`, `3.14+gil`
- `<implementation>`: `cpython` or `cp`; `<implementation>@<version>`: `cpython@3.12`; `cpython3.12` or `cp312`; `cpython>=3.12,<3.13`
- `<implementation>-<version>-<os>-<arch>-<libc>`: `cpython-3.12.3-macos-aarch64-none`
- Local interpreters: an executable path (`/opt/homebrew/bin/python3`), an executable name (`mypython3`) or an install dir (`/some/environment/`)

`UV_PYTHON_ARCH` picks an architecture independently (for example `x86_64`) while honoring the project's version request; a request that includes an architecture or names an executable takes precedence.

`.python-version` file:

- uv searches the working directory and each parent, then the user-level configuration directory. It does not search beyond project or workspace boundaries (except that user directory).
- Any request format works, but a plain version number is recommended for interoperability with other tools.
- Create one with `uv python pin`; create a global one with `uv python pin --global`.
- `--no-config` disables discovery of `.python-version` files.

Project commands honor `requires-python` in `pyproject.toml`: the first compatible Python is used unless a version is requested via `.python-version` or `--python`.

Find what a request resolves to: `uv python find` (first available executable) or `uv python find '>=3.11'`. By default it includes virtual environments: a `.venv` in the working directory or a parent, or `VIRTUAL_ENV`, wins over PATH executables. `uv python find --system` ignores virtual environments.

Implementation names are case-insensitive: cpython/cp, pypy/pp, graalpy/gp, pyodide.

## Verify

`uv python find '>=3.11'` prints the path of a matching interpreter; `uv python list 3.13` lists matching interpreters.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/python-versions). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
