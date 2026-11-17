---
id: computing-software.devops-ci-cd.build-systems.setuptools-scm-versioning
name: setuptools-scm-versioning
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, setuptools-scm, build-metadata, git-describe]
level: practitioner
status: docs-checked
description: "Derive Python package versions from git tags with setuptools-scm (or hatch-vcs): configuration, dev version format, CI shallow-clone pitfalls and exposing __version__."
sources: ["https://setuptools-scm.readthedocs.io/en/latest/", "https://github.com/pypa/setuptools-scm/tree/main/docs", "https://github.com/ofek/hatch-vcs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# setuptools-scm versioning

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=80", "setuptools-scm>=8"]
build-backend = "setuptools.build_meta"

[project]
name = "acme-tool"
dynamic = ["version"]

[tool.setuptools_scm]
version_file = "src/acme_tool/_version.py"     # generated, add to .gitignore
```
setuptools-scm requires setuptools 61 or later; its documentation recommends setuptools 80 or later.
Hatch users: the `hatch-vcs` plugin (`requires = ["hatchling", "hatch-vcs"]`, `[tool.hatch.version] source = "vcs"`) wraps the same machinery.

## Version scheme
- The default `version_scheme` is `guess-next-dev` and the default `local_scheme` is `node-and-date`.
- On tag `v1.4.2`: `1.4.2`.
- After commits past the tag: a `.devN` version of the next patch, with `+g<sha>` appended (for example `1.4.3.dev3+g9a1b2c3`); a dirty working tree also appends a date (`.dYYYYMMDD`).
- PyPI rejects local versions (`+g...`); publish only from tags or set
  `local_scheme = "no-local-version"` under `[tool.setuptools_scm]` for dev uploads.

## Runtime version
```python
from importlib.metadata import version
__version__ = version("acme-tool")
```
or import from the generated `_version.py`.

## CI pitfalls
- Shallow clones lack tags. setuptools-scm has a `git.pre_parse` option: `warn_on_shallow` (default), `fail_on_shallow` or `fetch_on_shallow`; a shallow clone is only fine when HEAD is exactly on a tag. In GitHub Actions use `actions/checkout` with `fetch-depth: 0`.
- Building from an sdist or archive without `.git`: setuptools-scm falls back to `PKG-INFO` (and `.git_archival.txt` for Git archives). To force a version, set `SETUPTOOLS_SCM_PRETEND_VERSION=1.4.2` (or `SETUPTOOLS_SCM_PRETEND_VERSION_FOR_<DIST_NAME>`).
- Check: `python -m setuptools_scm` prints the computed version.

## Verify
- [ ] A wheel built on tag `v1.4.2` carries version 1.4.2 (`acme_tool-1.4.2-...whl`).

## Checked
Date: 2026-10-25. Documentation: setuptools-scm `main` docs (pypa/setuptools-scm docs/usage.md, config.md, extending.md, overrides.md) and ofek/hatch-vcs README.
Confirmed: setuptools requirement (61 minimum, 80 recommended, `setuptools-scm>=8` appears in examples); `version_file`; default `guess-next-dev` and `node-and-date` schemes; `no-local-version` local scheme; `.dev` plus node and date output of `python -m setuptools_scm`; shallow-clone handling (`warn_on_shallow` default, `fail_on_shallow`, `fetch_on_shallow`); `SETUPTOOLS_SCM_PRETEND_VERSION` and the per-distribution variant; fallback order including `PKG-INFO`; hatch-vcs `build-system.requires` and `source = "vcs"`.
Removed: the claim that a shallow clone yields `0.1.dev1+g...` (the documentation describes warn/fail/fetch behaviour instead) and the `setuptools>=64` pin.
Method: documentation only; no commands were run.
