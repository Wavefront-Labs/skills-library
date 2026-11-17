---
id: computing-software.software-engineering.python.inspecting-sdist-and-wheel-contents
name: inspecting-sdist-and-wheel-contents
category: computing-software
field: software-engineering
product: python
tags: [python, py-packaging-publish, sdist-wheel-contents, wheel-unpack, packaging-audit, record-hashes]
level: practitioner
status: docs-checked
description: "Audit what you ship: know the layout of an sdist and a wheel (dist-info, METADATA, WHEEL, RECORD, tags, licence files) and check them before uploading."
sources: ["https://packaging.python.org/en/latest/specifications/binary-distribution-format/", "https://packaging.python.org/en/latest/specifications/source-distribution-format/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting sdist and wheel contents

## What the formats guarantee
- A wheel is a ZIP archive with the `.whl` extension, containing a single distribution nearly as it would be installed. File names inside are UTF-8.
- `{distribution}-{version}.dist-info/` holds the metadata: at minimum `METADATA`, `WHEEL` and `RECORD`. `METADATA` is the package metadata (same format as `PKG-INFO` in sdists). Licence files live in `{distribution}-{version}.dist-info/licenses/`.
- `WHEEL` describes the build: `Root-Is-Purelib` (true means the top level unpacks into purelib, otherwise platlib) and one or more `Tag:` lines such as `py3-none-any`.
- `RECORD` lists (almost) all files with their hashes. Every file except `RECORD` must include its hash (sha256 or better). Installers verify the hashes and installation fails if a file in the archive is not mentioned in `RECORD` or does not match.
- If there is data, the wheel also has `distribution-1.0.data/`.
- A current-format sdist is a `.tar.gz` named `{name}-{version}.tar.gz` with one top-level directory `{name}-{version}` holding the sources and a `pyproject.toml`; name and version must match the metadata. For metadata version 2.4 or newer it must contain the licence files listed by `License-File` in `PKG-INFO`.
- Tools must extract sdists with `tarfile.data_filter()` (`filter='data'`) or follow the spec's unpacking rules.

## Audit steps
1. Build the distributions, then list the sdist (`tar tzf dist/<name>-<version>.tar.gz`) and the wheel (any zip lister).
2. Read `METADATA` and `WHEEL` from the `.dist-info` directory; check the name, version, tags and `Root-Is-Purelib` against what you expect (a pure-Python tag `py3-none-any` on a package with compiled code is a mistake).
3. Check that data files you rely on are present in the wheel, and that tests, secrets or editor files are not.
4. Confirm the licence files are present in `dist-info/licenses/` and in the sdist.
5. Install the wheel in a clean virtual environment and test from a directory other than the repository root, so the source tree does not shadow the install.

## Gotchas
- The version in code and the `Version` in `METADATA` can drift; source it from one place.
- An sdist whose top-level directory or name/version do not match its metadata violates the format.

## Verify
- [ ] The wheel's `RECORD` covers every file; the wheel installs in a clean environment and a smoke test imports the package and reads one data file.

## Checked
Date: 2026-11-03. Confirmed against the Binary distribution format and Source distribution format specifications (wheel layout, `WHEEL` keys, `RECORD` rules, licences directory, sdist naming, layout, licence files and extraction filter rule). Removed as not in those pages: `check-wheel-contents` and its W001 code, `twine check --strict`, `MANIFEST.in`/`global-exclude`, setuptools `package-data`, `py.typed`, hatch options, `entry_points.txt`, cibuildwheel, PEP 639 `license =` syntax, `setuptools-scm` remark, `pip wheel` recipe.
Method: documentation only; no commands were run.
