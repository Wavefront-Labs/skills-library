---
id: computing-software.software-engineering.python.extras-and-dependency-groups
name: extras-and-dependency-groups
category: computing-software
field: software-engineering
product: python
tags: [python, python-extras, dependency-groups, optional-dependencies, pep-735, pyproject-toml, dev-dependencies]
level: practitioner
status: verified
description: "Split dependencies in pyproject.toml: optional-dependencies extras for users, PEP 735 dependency-groups for dev and test tooling, and installing each."
sources: ["https://packaging.python.org/en/latest/specifications/pyproject-toml/#dependencies-optional-dependencies", "https://peps.python.org/pep-0735/", "https://packaging.python.org/en/latest/specifications/dependency-groups/", "https://docs.astral.sh/uv/concepts/projects/dependencies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extras and dependency groups

**Goal:** a lean default install, opt-in features for users, and dev tooling that never
leaks into published metadata.

## Extras: optional features shipped in package metadata
```toml
[project]
dependencies = ["httpx>=0.27"]

[project.optional-dependencies]
s3 = ["boto3>=1.34"]
cli = ["typer>=0.12", "rich"]
all = ["mypkg[s3,cli]"]        # self-reference to combine extras
```
Users: `pip install "mypkg[s3]"` (quote: shells glob brackets). In code, import optional
deps lazily and fail with guidance:
```python
try:
    import boto3
except ImportError as e:
    raise ImportError("S3 support needs: pip install 'mypkg[s3]'") from e
```
Extras are public API: removing one breaks users' install commands.

## Dependency groups (PEP 735): never published
```toml
[dependency-groups]
test = ["pytest>=8", "pytest-cov"]
lint = ["ruff", "mypy"]
dev = [{include-group = "test"}, {include-group = "lint"}, "ipython"]
```
- Not part of the built wheel's metadata; for contributors and CI only.
- Install: `pip install --group dev` (pip 25.1+), `uv sync` (installs `dev` by default),
  `uv sync --group lint --no-dev`, `uv run --group test pytest`.
- Groups do not install the project itself; `uv sync` does that separately.

## Which one
| Dependency | Where |
|---|---|
| needed at runtime always | `project.dependencies` |
| runtime but optional feature | `optional-dependencies` |
| test/lint/docs/dev tools | `dependency-groups` |
| tool-specific legacy (Poetry `group.dev`, `tool.uv.dev-dependencies`) | migrate to `dependency-groups` |

Old habit of a `dev` extra (`pip install -e ".[dev]"`) still works but publishes your dev
tool list as a user-installable extra.

## Gotchas
- Extras names are normalised (`S3` == `s3`); keep them lowercase.
- Pin loosely in `dependencies`/extras (lower bounds), pin exactly in lockfiles, not here.
- Environment markers work in both: `"uvloop; sys_platform != 'win32'"`.

## Verify
- [ ] `pip install .` in a clean venv pulls only core deps (`pip list` check).
- [ ] Built wheel METADATA has `Provides-Extra` entries but no dev tools.
