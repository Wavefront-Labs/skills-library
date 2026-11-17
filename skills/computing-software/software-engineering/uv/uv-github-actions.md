---
id: computing-software.software-engineering.uv.uv-github-actions
name: uv-github-actions
category: computing-software
field: software-engineering
product: uv
tags: [uv, github-actions, ci, setup-uv, python-matrix, uv-cache, trusted-publishing, private-repos]
level: practitioner
status: docs-checked
description: "Use astral-sh/setup-uv in GitHub Actions for pinned uv, Python matrices, locked sync, caching, private repos and trusted publishing to PyPI."
sources: [https://docs.astral.sh/uv/guides/integration/github/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv in GitHub Actions

Goal: a CI workflow that installs uv, Python and the project, with caching and release publishing.

## Method

Install uv with the official action, pinning the uv version (pin the action to a commit SHA as the page does):

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@<commit-sha> # v9.0.0
  with:
    version: "0.13.7"
```

Python: `run: uv python install` respects the project's pinned version. Alternatively `actions/setup-python` with `python-version-file: ".python-version"` (the pin) or `"pyproject.toml"` (latest compatible with `requires-python`).

Matrix: pass the version to setup-uv, which overrides `pyproject.toml` and `.python-version`:

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
steps:
  - uses: astral-sh/setup-uv@<commit-sha>
    with:
      python-version: ${{ matrix.python-version }}
```

Without setup-uv set `UV_PYTHON` in `env` to the matrix value.

Sync and run: `uv sync --locked --all-extras --dev`, then `uv run pytest tests`. `UV_PROJECT_ENVIRONMENT` can target the system Python instead of a venv.

### Caching

`with: enable-cache: true` on setup-uv. Or manually: set `UV_CACHE_DIR` to a constant path, restore it with `actions/cache` (key from `hashFiles('uv.lock')`, or `requirements.txt` with `uv pip`), and finish the job with `uv cache prune --ci`. On non-ephemeral self-hosted runners put `UV_CACHE_DIR` inside the workspace and clear it with a post-job hook running `uv cache clean` (hook set through `ACTIONS_RUNNER_HOOK_JOB_STARTED`).

### uv pip

Needs a venv by default; use `--system`, or `UV_SYSTEM_PYTHON: 1` at workflow, job or step scope. Opt out with `--no-system`.

### Private repos

Store a PAT as a repository secret, then run `gh auth login --with-token` (secret piped on stdin) followed by `gh auth setup-git` so Git uses it for github.com.

### Publishing to PyPI

Use two jobs. `build` (permissions `contents: read`) runs `uv build` and uploads `dist/`; optional smoke tests use `uv run --isolated --no-project --with dist/*.whl tests/smoke_test.py`. `publish` (needs build, `environment: name: pypi`, permissions `id-token: write`) downloads `dist/`, runs `astral-sh/attest-action`, then `uv publish`. Trigger on version tags such as `v[0-9]+.[0-9]+.[0-9]+`. Create the `pypi` environment in the repo's Settings and add a Trusted Publisher in the PyPI project settings with matching fields. Splitting jobs keeps the publish credential away from build steps. Then `git tag -a v0.1.0 -m v0.1.0` and `git push --tags`.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/integration/github). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
