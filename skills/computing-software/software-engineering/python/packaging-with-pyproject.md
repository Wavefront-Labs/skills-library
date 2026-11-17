---
id: computing-software.software-engineering.python.packaging-with-pyproject
name: packaging-with-pyproject
category: computing-software
field: software-engineering
product: python
tags: [python, pyproject-toml, packaging, pep-621, pep-517, src-layout, hatchling, setuptools, flit, uv, uv-lock, pip, pip-tools, venv, virtualenv, lockfile, version-pinning, requires-python, pypi, twine, trusted-publishing, oidc, github-actions, wheel, sdist, poetry, py-packaging-build]
level: practitioner
status: verified
description: "Package a Python project with pyproject.toml and a src layout, manage venvs and lockfiles with uv or pip, and publish to PyPI using trusted publishing instead of API tokens."
sources: ["Python Packaging User Guide (packaging.python.org) - Writing your pyproject.toml", "PEP 621 Storing project metadata in pyproject.toml", "PEP 517 / PEP 518 build system specification", "PyPI docs - Trusted Publishers", "uv documentation (Astral) - projects and lockfiles"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Packaging with pyproject.toml — one config, reproducible installs, token-free publishing

**Goal:** a project that installs the same way on every machine, builds a correct wheel,
and publishes to PyPI from CI without a long-lived secret.

## 1. Layout
```
<PROJECT_ROOT>/
  pyproject.toml
  src/mypkg/__init__.py
  src/mypkg/py.typed        # if you ship type hints
  tests/
```
The `src/` layout forces tests to run against the *installed* package, so a missing
file in the wheel fails in CI instead of on a user's machine. No `setup.py` or
`setup.cfg` needed for new projects.

## 2. Minimal pyproject.toml
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mypkg"
version = "1.4.0"            # or dynamic = ["version"] with hatch-vcs / setuptools-scm
description = "One line."
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"              # SPDX expression (PEP 639); older backends want a table
dependencies = ["httpx>=0.27", "pydantic>=2,<3"]

[project.optional-dependencies]
cli = ["typer>=0.12"]

[project.scripts]
mypkg = "mypkg.cli:main"

[dependency-groups]          # PEP 735: dev-only, never published
dev = ["pytest>=8", "ruff", "mypy"]
```
Backends: **hatchling** (simple, sensible defaults), **setuptools** (>= 61 reads
`[project]`; needed for C extensions with legacy config), **flit-core** (pure Python,
minimal), **uv_build** (Astral's backend; newer — check maturity for your case),
**maturin** / **scikit-build-core** for Rust / C++ extensions.

## 3. Pinning philosophy
- **Libraries:** loose lower bounds in `dependencies` (`>=2.1`), upper caps only for
  known breaks. Over-pinning a library makes it uninstallable next to others.
- **Applications/services:** loose ranges in pyproject plus an exact **lockfile** for
  deploys. Never exact-pin `dependencies` of something others import.
- `requires-python` lower bound is enforced by installers; don't add an upper bound
  (`<4`) — resolvers treat it badly.

## 4. Environments and locking
**uv** (fast, all-in-one, the 2026 default for many teams):
```
uv venv                    # .venv with the right interpreter (uv python install 3.12)
uv sync                    # install project + dev group from uv.lock
uv add httpx               # edit pyproject + relock
uv lock --upgrade-package httpx
uv sync --locked           # CI: fail if uv.lock is stale
uv run pytest
```
**pip-only** equivalent: `python -m venv .venv`, `pip install -e . --group dev`
(pip >= 25.1 for `--group`; otherwise a requirements-dev file), and
`pip-compile --generate-hashes` (pip-tools) to produce a hashed `requirements.txt`
installed with `pip install --require-hashes -r requirements.txt`.
PEP 751 (`pylock.toml`, status Final) is the standard lockfile format; tool support is still
rolling out — check before relying on it.

## 5. Build and check
```
uv build                       # or: python -m build  -> dist/*.whl + dist/*.tar.gz
uvx twine check dist/*         # README renders, metadata valid
unzip -l dist/*.whl            # did data files / py.typed make it in?
```
Test the built wheel in a clean venv, not the editable install.

## 6. Publish with trusted publishing (no API token)
1. On PyPI: project › Settings › Publishing › add a trusted publisher: owner, repo,
   workflow filename (e.g. `release.yml`), environment name (e.g. `pypi`). For a new
   project use a "pending publisher".
2. Workflow job:
```yaml
jobs:
  publish:
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write          # OIDC token for PyPI
      contents: read
    steps:
      - uses: actions/checkout@v4     # majors move (checkout v7, setup-uv v10 when reviewed); pin to a sha in practice
      - uses: astral-sh/setup-uv@v6
      - run: uv build
      - uses: pypa/gh-action-pypi-publish@release/v1
```
The action mints a short-lived token; recent versions also generate PEP 740
attestations by default. Protect the `pypi` environment with required reviewers.
Rehearse against TestPyPI with a separate publisher.

## Gotchas
- Versions on PyPI are immutable: a bad 1.4.0 can be yanked, never replaced. Bump.
- Package name normalisation: `My_Pkg`, `my-pkg`, `my.pkg` are the same project on PyPI.
- Non-Python files (templates, JSON) in `src/mypkg/` are included by hatchling but may
  need `package-data`/`MANIFEST.in` with setuptools — verify with `unzip -l`.
- `dynamic = ["version"]` from git tags gives `0.1.dev1+g<sha>` in shallow CI clones;
  use `fetch-depth: 0`.
- A forgotten `--locked`/`--frozen` in CI lets `uv sync` silently re-resolve.
- Editable installs hide missing-file bugs; test the wheel.

## Verify
- [ ] `uv build` (or `python -m build`) produces a wheel and sdist with no warnings.
- [ ] `twine check dist/*` passes; the wheel contains every runtime file.
- [ ] Tests pass against the installed wheel in a fresh venv.
- [ ] CI installs with `uv sync --locked` (or `--require-hashes`) and fails on a stale lock.
- [ ] No PyPI API token stored in repo secrets; trusted publisher configured and environment-protected.
- [ ] `requires-python` matches the oldest version you actually test.
