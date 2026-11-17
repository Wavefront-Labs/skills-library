---
id: creative-arts.animation.scripting.rez-package-environments
name: rez-package-environments
category: creative-arts
field: animation
product: scripting
tags: [rez, pipeline-python, dcc-python, package-manager, environment-resolve, package-py, studio-environment, versioning, launcher]
level: advanced
status: draft
description: "Manage DCC and pipeline tool versions per show with Rez: package.py definitions, resolving environments, release vs local packages, and launching apps."
sources:
  - https://rez.readthedocs.io/en/stable/
  - https://rez.readthedocs.io/en/stable/package_definition.html
  - https://github.com/AcademySoftwareFoundation/rez
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rez package environments

**Goal:** show A runs Maya 2024 + pipeline 3.2 + USD 23.11 while show B runs Maya 2025 + pipeline 4.0,
on the same workstation, with no manual PATH editing. Rez (ASWF) resolves a set of package requests
into an environment.

## A package

```python
# <REPO>/pipeline_tools/package.py
name = "pipeline_tools"
version = "3.2.0"
requires = ["python-3.10", "pyside2", "~maya-2024"]   # ~ = weak: only constrains if maya is requested
build_command = "python {root}/build.py {install}"    # or None for pure python with rezbuild
def commands():
    env.PYTHONPATH.append("{root}/python")
    env.PIPELINE_ROOT = "{root}"
    alias("publish", "python {root}/bin/publish.py")
```

Release: `rez-build --install` (local) or `rez-release` (to the studio's release path, usually tied
to a git tag).

## Resolving and running

```bash
rez-env maya-2024 pipeline_tools-3.2 usd -- maya
rez-env show_x                       # a "show package" whose requires pins the show's versions
rez-context                          # inside a resolved shell: shows what was resolved
```

Show packages are the practical pattern: `show_x/package.py` with `requires = ["maya-2024.2",
"pipeline_tools-3.2", "arnold-7.2"]`. Artists launch through a launcher that calls `rez-env show_x -- maya`.

## Configuration

- `REZ_PACKAGES_PATH`: local packages first, then studio release path.
- `rezconfig.py`: packages paths, release path, caching (`package_cache_path` for local caching of
  network packages; big speedup on Windows).

## Gotchas

- DCCs themselves are usually "wrapper" packages (commands set PATH to an installed Maya), not rebuilt.
- Conflicting requirements fail the resolve with a readable conflict graph (`rez-env --fail-graph`);
  fix by loosening ranges rather than forcing.
- Windows path lengths and network latency make resolves slow; enable memcached/package caching.

## Verify

`rez-env show_x -- python -c "import pipeline_tools, sys; print(pipeline_tools.__file__)"` prints the
expected version path; the same command for show_y prints the other version.
