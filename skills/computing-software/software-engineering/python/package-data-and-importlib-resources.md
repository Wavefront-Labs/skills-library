---
id: computing-software.software-engineering.python.package-data-and-importlib-resources
name: package-data-and-importlib-resources
category: computing-software
field: software-engineering
product: python
tags: [python, package-data, importlib-resources, manifest-in, data-files, zipapp, wheel-contents]
level: practitioner
status: verified
description: "Ship non-code files (templates, schemas, SQL) inside a package, include them in sdist and wheel with hatchling or setuptools, and load them with importlib.resources."
sources: ["https://docs.python.org/3/library/importlib.resources.html", "https://setuptools.pypa.io/en/latest/userguide/datafiles.html", "https://hatch.pypa.io/latest/config/build/", "https://packaging.python.org/en/latest/guides/using-manifest-in/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Package data and importlib.resources

**Goal:** data files that are present after `pip install` from a wheel, and code that
finds them regardless of install location, zip imports or cwd.

## Put data inside the package
```
src/mypkg/__init__.py
src/mypkg/templates/email.html
src/mypkg/schema/v1.json
```
Data outside the package directory (top-level `data/`) is not importable as a resource
and is awkward to ship; move it in.

## Make sure the build includes it
**hatchling:** files inside the package dir are included automatically if tracked by
git / not ignored. Exclude or force:
```toml
[tool.hatch.build.targets.wheel]
packages = ["src/mypkg"]
[tool.hatch.build.targets.wheel.force-include]
"assets/logo.png" = "mypkg/assets/logo.png"
```
**setuptools:** `include-package-data = true` (default with pyproject) includes files that
are in the sdist (tracked by git with setuptools-scm, or listed in `MANIFEST.in`):
```toml
[tool.setuptools.package-data]
mypkg = ["templates/*.html", "schema/*.json"]
```

## Load with importlib.resources (3.9+ API)
```python
from importlib.resources import files, as_file
import json

schema = json.loads(files("mypkg.schema").joinpath("v1.json").read_text(encoding="utf-8"))
tpl = (files("mypkg") / "templates" / "email.html").read_text(encoding="utf-8")

# APIs that need a real filesystem path (e.g. a C library):
with as_file(files("mypkg") / "models" / "weights.bin") as path:
    lib.load(str(path))      # temp file is extracted if the package is zipped
```
Avoid `os.path.join(os.path.dirname(__file__), ...)`: breaks for zip imports/zipapps and
PyInstaller-style bundles, and `pkg_resources` was removed from setuptools in v82.0.0 (`import pkg_resources` fails on 84.0.0).

## Gotchas
- Files present in the source tree but missing in the wheel is the #1 bug: works in
  editable installs, fails in production.
- `files()` takes a package (importable) name; subdirectories without `__init__.py` work as
  traversable paths, but pass the top package and use `/`.
- Large binaries bloat every install; consider downloading on first use with caching.
- Writing into package directories at runtime fails on read-only installs; write to
  `platformdirs.user_cache_dir()` instead.

## Verify
- [ ] `unzip -l dist/*.whl | grep templates/` lists the data files.
- [ ] Tests run against the installed wheel (`nox`/`tox` with non-editable install) load every resource.
