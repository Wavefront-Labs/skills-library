---
id: computing-software.software-engineering.python.single-sourcing-the-package-version
name: single-sourcing-the-package-version
category: computing-software
field: software-engineering
product: python
tags: [python, setuptools-scm, dynamic-version, importlib-metadata, hatch-vcs, version-from-git-tag]
level: practitioner
status: verified
description: "Keep one source of truth for a package version: static in pyproject, dynamic from a file, or from git tags via setuptools-scm/hatch-vcs, read at runtime via importlib.metadata."
sources: ["https://packaging.python.org/en/latest/discussions/single-source-version/", "https://setuptools-scm.readthedocs.io/en/latest/", "https://github.com/ofek/hatch-vcs", "https://docs.python.org/3/library/importlib.metadata.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single-sourcing the package version

**Goal:** the version in the wheel, `mypkg.__version__`, the git tag and the changelog
never disagree.

## Option A: static in pyproject (simplest)
```toml
[project]
version = "1.4.2"
```
Bump with `uv version --bump minor` / `hatch version minor` and tag in the same commit.

## Option B: from git tags (no version commits)
```toml
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"
[project]
dynamic = ["version"]
[tool.hatch.version]
source = "vcs"
[tool.hatch.build.hooks.vcs]
version-file = "src/mypkg/_version.py"     # optional generated file
```
setuptools equivalent:
```toml
[build-system]
requires = ["setuptools>=64", "setuptools-scm>=8"]
[project]
dynamic = ["version"]
[tool.setuptools_scm]
```
Tag `v1.4.2` -> version `1.4.2`; commits after it -> `1.4.3.dev4+g1a2b3c4` (PEP 440 dev
version with local part; PEP 440 says local versions SHOULD NOT be published upstream, so
set `local_scheme = "no-local-version"` for index uploads: tested, `1.4.3.dev2+g<sha>` became `1.4.3.dev2`).

CI gotchas: shallow clones have no tags -> version `0.1.dev1`. Use
`actions/checkout` with `fetch-depth: 0` (or `fetch-tags: true`). Building from an sdist
works because the version is baked into `PKG-INFO`.

## Reading the version at runtime
```python
# mypkg/__init__.py
from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("mypkg")        # distribution name, not import name
except PackageNotFoundError:               # running from a source tree without install
    __version__ = "0+unknown"
```
Reads installed metadata, so it reflects what pip installed. Avoid parsing pyproject.toml
at runtime (not shipped in wheels).

## Option C: from a file attribute
`[tool.hatch.version] path = "src/mypkg/__about__.py"` reads `__version__ = "1.4.2"`.
Fine, but now the file is the single source; don't also set `project.version`.

## Verify
- [ ] `python -m build && unzip -p dist/*.whl '*/METADATA' | grep ^Version` matches the tag.
- [ ] `python -c "import mypkg; print(mypkg.__version__)"` in a clean venv matches too.
