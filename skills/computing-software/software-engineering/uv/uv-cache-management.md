---
id: computing-software.software-engineering.uv.uv-cache-management
name: uv-cache-management
category: computing-software
field: software-engineering
product: uv
tags: [uv, caching, cache-dir, cache-clean, cache-prune, refresh, reinstall, no-cache]
level: practitioner
status: docs-checked
description: "Understand uv cache semantics per dependency kind, refresh or clear the cache, pick the cache directory, and know cache safety and versioning rules."
sources: [https://docs.astral.sh/uv/concepts/cache/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv cache management

Goal: fix stale-cache problems and manage the cache directory safely.

## Method

Cache semantics:

- Registry: respects HTTP caching headers. Direct URL: headers plus the URL.
- Git: keyed on the resolved commit hash (so `uv pip compile` pins Git dependencies to a commit).
- Local: last-modified time of the `.whl` or `.tar.gz`; for directories, of `pyproject.toml`, `setup.py` or `setup.cfg`.
- Flat indexes (`--find-links`): treated as immutable, cached by file name.

Escape hatches:

- `uv cache clean` clears everything (directory and lock file remain); `uv cache clean ruff` clears one package.
- `uv cache prune` removes unused entries and all centralized project environments (recreated as needed); safe to run periodically.
- `--refresh` revalidates all cached data on any command (`uv sync --refresh`); `--refresh-package ruff` for one package.
- `--reinstall` ignores installed versions; consider `uv cache clean <package-name>` first.
- Local directories passed explicitly (`uv pip install .`) are always rebuilt and reinstalled.

Cache directory order: (1) temporary directory with `--no-cache`; (2) `--cache-dir`, `UV_CACHE_DIR` or `tool.uv.cache-dir`; (3) system default, `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on Unix, under `%LOCALAPPDATA%` on Windows. uv always needs a cache; `--no-cache` still uses a temporary one for that invocation. Prefer `--refresh` over `--no-cache`, since it updates the cache for later runs. Put the cache on the same file system as the environment so uv can link instead of copy.

Locking: concurrent uv commands are safe, including against one virtual environment (file lock on install). Cache-modifying `uv cache` commands wait for other uv processes with a 5 minute timeout, changed by `UV_LOCK_TIMEOUT`; `--force` ignores the lock only if nothing else uses the cache.

Space estimates: the `cache-physical-space` preview feature (`uv cache clean --preview-features cache-physical-space`) accounts for hardlinks and copy-on-write clones on macOS and Linux.

## Gotchas

- Never modify the cache directly (removing files or directories).
- The cache is split into versioned buckets (wheels, source distributions, Git). Multiple uv versions can share a cache; if the bucket version changed between releases (for example metadata v12 to v13 in uv 0.4.13), entries are not shared and may duplicate.
- Interrupted HTTP cache refreshes are detected and re-downloaded; with `--offline` an affected entry is unavailable until refreshed online.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/cache). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
