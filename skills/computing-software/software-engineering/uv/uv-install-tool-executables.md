---
id: computing-software.software-engineering.uv.uv-install-tool-executables
name: uv-install-tool-executables
category: computing-software
field: software-engineering
product: uv
tags: [uv, uv-tool, tool-environments, tools-concepts, upgrade, path, executables]
level: practitioner
status: docs-checked
description: "Manage persistent uv tools: tool install, environments, upgrade, --with and --with-executables-from, executable directory on PATH, --force and Python links."
sources: [https://docs.astral.sh/uv/concepts/tools/, https://docs.astral.sh/uv/guides/tools/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing and maintaining uv tools

Goal: install CLI tools persistently so their executables are on the PATH, and keep them current.

## Method

- Install: `uv tool install ruff`. Versions and sources work directly: `uv tool install 'httpie>0.1.0'`, `uv tool install git+https://github.com/httpie/cli`, `uv tool install ruff@latest`, `uv tool install ruff@0.6.0`. Add `--lfs` for Git LFS sources and `--python 3.10` for a Python.
- Prefer `uvx` unless other programs need the tool (a script you do not control, a Docker image).
- Extra packages: `uv tool install mkdocs --with mkdocs-material` (repeatable, `-w` shorthand). `--with` adds dependencies but not their executables.
- Executables from related packages: `uv tool install --with-executables-from ansible-core,ansible-lint ansible`. Executables of ordinary dependencies are not installed.
- Executables are every console entry point, script entry point and binary script; they are symlinked into the executable directory on Unix and copied on Windows. That directory must be on PATH. If not, uv warns and `uv tool update-shell` adds it to common shell config files.
- Upgrade: `uv tool upgrade ruff`, `uv tool upgrade --all`, one dependency with `uv tool upgrade black --upgrade-package click`. Upgrades respect the constraints and settings given at install (for example `--prerelease allow`). To change constraints, reinstall: `uv tool install black>=24`. Use `--reinstall` or `--reinstall-package click` to force reinstalls. Upgrades reinstall executables even if unchanged.
- Python: `uv tool upgrade --python 3.10 ruff`.

## Gotchas

- Tool environments live in the uv tools directory, are removed only when the tool is uninstalled, and fail to run if deleted by hand. Never mutate them (for example with pip).
- Uninstalling the Python a tool uses breaks that tool environment.
- Tool Python selection ignores `.python-version` files and `requires-python` from pyproject.toml.
- `uv tool install` will not overwrite executables not installed by uv (for example from pipx); `--force` overrides.
- A `--with` version that conflicts with the tool's requirements makes resolution fail.
- Once installed, `uvx ruff` uses the installed version; `uvx ruff@latest` or `uvx --isolated ruff` ignores it. Without an installed copy, `uvx` caches the version from its first run until the cache is pruned or refreshed.

## Verify

After `uv tool install ruff`, `ruff --version` prints the version, while `python -c "import ruff"` fails.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/tools; guides/tools). Removed or changed: reworded the tool-environment cache claim to what the page states (removed only on uninstall).

Method: documentation only; no commands were run.
