---
id: computing-software.software-engineering.uv.uv-storage-installer-env
name: uv-storage-installer-env
category: computing-software
field: software-engineering
product: uv
tags: [uv, storage-directories, xdg, installer-env, install-path, uv-install-dir, uv-no-modify-path, uv-tool-dir]
level: practitioner
status: docs-checked
description: "Locate and relocate uv's cache, data, Python, tool and executable directories, and control the standalone installer with its environment variables."
sources: [https://docs.astral.sh/uv/reference/storage/, https://docs.astral.sh/uv/reference/installer/, https://docs.astral.sh/uv/concepts/cache/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv storage directories and installer variables

Goal: know where uv keeps things and how to move them.

## Method

uv follows XDG conventions on Linux and macOS and the Known Folder scheme on Windows. For each location the first existing environment variable in the list wins.

Unix lookup order:

- Temporary: `$TMPDIR`, then `/tmp`
- Cache: `$XDG_CACHE_HOME/uv`, then `$HOME/.cache/uv`
- Persistent data: `$XDG_DATA_HOME/uv`, then `$HOME/.local/share/uv`, then `$CWD/.uv`
- User configuration: `$XDG_CONFIG_HOME/uv`, then `$HOME/.config/uv`
- System configuration: `$XDG_CONFIG_DIRS/uv`, then `/etc/uv`
- Executables (should be on PATH): `$XDG_BIN_HOME`, then `$XDG_DATA_HOME/../bin`, then `$HOME/.local/bin`

Windows uses `%TMP%`/`%TEMP%`, `%LOCALAPPDATA%` (cache), `%APPDATA%` (data and user config), `%PROGRAMDATA%` (system) and `%XDG_BIN_HOME%` or `%USERPROFILE%` based locations.

Per data type:

| Data | Default | Show | Override |
|---|---|---|---|
| Dependency cache | cache directory | `uv cache dir` | `--cache-dir`, `UV_CACHE_DIR` |
| Managed Pythons | `python/` in data directory | `uv python dir` | `UV_PYTHON_INSTALL_DIR` |
| Python executables | executable directory | `uv python dir --bin` | `UV_PYTHON_BIN_DIR` |
| Tools | `tools/` in data directory | `uv tool dir` | `UV_TOOL_DIR` |
| Tool executables | executable directory | `uv tool dir --bin` | `UV_TOOL_BIN_DIR` |
| uv and uvx binaries (standalone installer) | executable directory | | `UV_INSTALL_DIR` |
| Project venv | `.venv` next to `pyproject.toml` | | `UV_PROJECT_ENVIRONMENT` |

Script environments live in the cache directory. With the `centralized-project-envs` preview feature, project environments go to the cache too and `uv cache clean` or `uv cache prune` remove them (recreated when needed).

### Installer variables

```console
$ curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/custom/path" sh
$ curl -LsSf https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 sh
$ curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="/custom/path" sh
```

- `UV_INSTALL_DIR` moves only the binary; data (cache, Pythons, tools) stays in the default locations.
- `UV_NO_MODIFY_PATH=1` stops shell profile edits, and later `uv self update` will not edit them either.
- `UV_UNMANAGED_INSTALL` is for ephemeral environments such as CI: installs to the path, leaves profiles and environment untouched, and disables `uv self update`.
- Script options can be passed directly, for example `... | sh -s -- --help`; environment variables are recommended as they work across platforms.

## Gotchas

- For best performance keep the cache on the same filesystem as virtual environments.
- Changing the Python install directory does not update existing virtual environments; recreate them.
- With the cache disabled, uv uses a temporary directory instead.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (reference/storage; reference/installer; concepts/cache). Removed or changed: fixed the user configuration path to $HOME/.config/uv; added the cache concept page to sources, where --cache-dir and UV_CACHE_DIR are documented.

Method: documentation only; no commands were run.
