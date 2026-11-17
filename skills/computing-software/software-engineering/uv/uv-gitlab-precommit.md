---
id: computing-software.software-engineering.uv.uv-gitlab-precommit
name: uv-gitlab-precommit
category: computing-software
field: software-engineering
product: uv
tags: [uv, gitlab, ci, gitlab-ci, pre-commit, hooks, uv-lock, uv-export, pip-compile]
level: practitioner
status: docs-checked
description: "Run uv in GitLab CI with the official image and a lockfile-keyed cache, and add uv-pre-commit hooks for uv-lock, uv-export and pip-compile."
sources: [https://docs.astral.sh/uv/guides/integration/gitlab/, https://docs.astral.sh/uv/guides/integration/pre-commit/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv in GitLab CI/CD and pre-commit

Goal: CI jobs with a uv image and cache, and hooks that keep lock and requirements files current.

## Method

### GitLab image

Use an official uv image variant that has a shell so the runner can execute `script`:

```yaml
variables:
  UV_VERSION: "0.13.7"
  PYTHON_VERSION: "3.12"
  BASE_LAYER: trixie-slim
  # separate mountpoint for the build directory: copy instead of hard links
  UV_LINK_MODE: copy

uv:
  image: ghcr.io/astral-sh/uv:$UV_VERSION-python$PYTHON_VERSION-$BASE_LAYER
  script:
    # your uv commands
```

### Cache

```yaml
uv-install:
  variables:
    UV_CACHE_DIR: .uv-cache
  cache:
    - key:
        files:
          - uv.lock
      paths:
        - $UV_CACHE_DIR
  script:
    # your uv commands
  after_script:
    - uv cache prune --ci
```

`uv cache prune --ci` at the end reduces cache size. With the pip interface key on `requirements.txt` or `pyproject.toml` instead of `uv.lock`.

### uv pip

A venv is required by default. Use `--system` on each call or define `UV_SYSTEM_PYTHON: 1` under top-level `variables`. Opt out with `--no-system`.

### pre-commit hooks

The official hooks come from `https://github.com/astral-sh/uv-pre-commit`. Set `rev` to the uv version and add to `repos` in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/uv-pre-commit
    rev: 0.13.7
    hooks:
      - id: uv-lock
```

Hook ids:

- `uv-lock` keeps `uv.lock` current when `pyproject.toml` changes.
- `uv-export` keeps `requirements.txt` in sync with `uv.lock`.
- `pip-compile` compiles requirements, for example `args: [requirements.in, -o, requirements.txt]`.

For other files change `args` and `files`:

```yaml
      - id: pip-compile
        args: [requirements-dev.in, -o, requirements-dev.txt]
        files: ^requirements-dev\.(in|txt)$
```

To cover several files, add one `pip-compile` entry per file, each with its own `name`, `args` and `files`.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/integration/gitlab; guides/integration/pre-commit). Removed or changed: removed an invented Verify line.

Method: documentation only; no commands were run.
