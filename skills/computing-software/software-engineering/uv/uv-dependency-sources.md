---
id: computing-software.software-engineering.uv.uv-dependency-sources
name: uv-dependency-sources
category: computing-software
field: software-engineering
product: uv
tags: [uv, dependency-sources, tool-uv-sources, git, path, url, index, workspace, python]
level: practitioner
status: docs-checked
description: "Declare git, URL, path, index and workspace sources in tool.uv.sources, with markers for per-platform and multiple sources and --no-sources to ignore them."
sources: [https://docs.astral.sh/uv/concepts/projects/dependencies/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tool.uv.sources

Goal: point a dependency at something other than the default index during development.

## Method

Keep the name in `project.dependencies`; add the source in `[tool.uv.sources]`. Supported: index, git, url, path, workspace.

- Index: `uv add torch --index pytorch=https://download.pytorch.org/whl/cpu` writes `torch = { index = "pytorch" }` plus a `[[tool.uv.index]]` with `name` and `url`. An `index` source pins the package to that index. `explicit = true` on the index limits it to packages that name it in sources. Selecting an already configured index by name is preview: `uv add --preview-features index-by-name torch --index pytorch`.
- Git: `uv add git+https://github.com/encode/httpx` (or `git+ssh://git@github.com/...`). Refine with `--tag 0.27.0`, `--branch main`, `--rev <sha>`, or `#subdirectory=libs/langchain`. In TOML: `{ git = "...", tag = "0.27.0" }`, `branch`, `rev`, `subdirectory`.
- Git LFS: `uv add --lfs git+...` writes `lfs = true`. Omitted means `UV_GIT_LFS` applies; default is not to fetch LFS objects. Git LFS must be installed or the build can fail.
- URL: `https://` link to a `.whl`, `.tar.gz` or `.zip`; written as `{ url = "..." }`, optional `subdirectory`.
- Path: wheel, sdist or a directory with a `pyproject.toml`: `uv add ./foo-0.1.0-py3-none-any.whl`, `uv add ~/projects/bar/`. Path directories are not editable unless `uv add --editable ../projects/bar/` (`editable = true`).
- Workspace: `foo = { workspace = true }`, with the member in `[tool.uv.workspace] members`; always editable. `workspace = "../other-workspace"` targets another workspace.
- Per platform: add `marker = "sys_platform == 'darwin'"` to a source; other platforms fall back to PyPI.
- Multiple sources: a list of tables separated by markers, e.g. two `index` entries keyed on `platform_system == 'Darwin'` and `'Linux'`, or `extra = "cpu"` / `extra = "gpu"` for optional dependencies.
- Ignore sources: `uv lock --no-sources` (also stops workspace member discovery).

## Gotchas

- Only uv reads `tool.uv.sources`; other tools see just the standard tables.
- Directory path dependencies are built and installed as packages by default.

## Verify

`uv add git+https://github.com/encode/httpx --tag 0.27.0` yields `httpx = { git = "https://github.com/encode/httpx", tag = "0.27.0" }` under `[tool.uv.sources]`.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/dependencies). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
