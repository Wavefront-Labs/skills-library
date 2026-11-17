---
id: computing-software.software-engineering.uv.uv-run-tools-uvx
name: uv-run-tools-uvx
category: computing-software
field: software-engineering
product: uv
tags: [uv, uvx, tool-run, tools, tools-guide, from, with, version-pinning]
level: practitioner
status: docs-checked
description: "Run Python command-line tools in throwaway environments with uvx: --from, command@version, extras, git sources, plugins via --with and --python."
sources: [https://docs.astral.sh/uv/guides/tools/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running tools with uvx

Goal: invoke a tool published as a Python package without installing it. `uvx` is an alias for `uv tool run`; the two are exactly equivalent. Tools run in temporary, isolated environments.

## Method

- Run: `uvx ruff`; arguments follow the tool name, e.g. `uvx pycowsay hello from uv`.
- Command differs from package name: `uvx --from httpie http`.
- Versions: `uvx ruff@0.3.0 check` (exact only), `uvx ruff@latest check`, `uvx --from 'ruff==0.3.0' ruff check`, or a range with `uvx --from 'ruff>0.2.0,<0.3.0' ruff check`. The `@` syntax cannot express anything but an exact version (or `latest`).
- Extras: `uvx --from 'mypy[faster-cache,reports]' mypy --xml-report mypy_report`; combine with a version as `'mypy[faster-cache,reports]==1.13.0'`.
- Other sources via `--from`:
  - `git+https://github.com/httpie/cli`
  - branch: `git+https://github.com/httpie/cli@master`
  - tag: `...@3.2.4`
  - commit: `...@2843b87`
  - Git LFS: `uvx --lfs --from git+https://github.com/astral-sh/lfs-cowsay lfs-cowsay`
- Plugins or extra packages: `uvx --with mkdocs-material mkdocs --help`.
- Python: `uvx --python 3.10 ruff`. By default uv uses the first interpreter it finds.
- Legacy Windows setuptools scripts (`.ps1`, `.cmd`, `.bat`, tried in that order): `uv tool run --from nuitka==2.6.7 nuitka --version`.

## Gotchas

- In a project, a tool that needs the project installed (pytest, mypy with a `src` layout) should run via `uv run`, not `uvx`, because uvx isolates it from the project. With a flat layout `uvx` is fine; `uv run` then only helps if you want to pin the tool in project dependencies.
- Installing instead (`uv tool install`) is covered by a separate skill; `uv tool install` does not make a tool's modules importable (`python -c "import ruff"` fails).

## Verify

`uvx pycowsay hello from uv` prints the cow drawing around "hello from uv" in the guide's example.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/tools). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
