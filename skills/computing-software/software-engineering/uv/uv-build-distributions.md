---
id: computing-software.software-engineering.uv.uv-build-distributions
name: uv-build-distributions
category: computing-software
field: software-engineering
product: uv
tags: [uv, uv-build, sdist-wheel, build-constraint, require-hashes, dist, build-frontend, python]
level: practitioner
status: docs-checked
description: "Build sdists and wheels with uv build, limit to one kind, pin build requirements with --build-constraint and hashes, and mark a project as not uploadable."
sources: [https://docs.astral.sh/uv/concepts/projects/build/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building distributions with uv build

Goal: produce an sdist and wheel in `dist/`, optionally with hash-verified build requirements.

## Method

- `uv build` acts as a build frontend: it picks the Python version and invokes the backend declared in `[build-system]`. Included files and filenames are decided by the backend.
- `uv build` builds the project in the current directory into `dist/`, e.g. `example-0.1.0-py3-none-any.whl` and `example-0.1.0.tar.gz`. A path builds elsewhere: `uv build path/to/project`.
- It builds the sdist first, then the wheel from that sdist. Limit with `--sdist`, `--wheel`, or both: `uv build --sdist --wheel`.
- Constrain build requirements: `uv build --build-constraint constraints.txt --require-hashes`, with `constraints.txt` such as `setuptools==68.2.2 --hash=sha256:...`. Use `--require-build-hashes` to demand hashes for every build dependency, transitive ones included.
- Project-wide hashes in `pyproject.toml`:

```toml
[tool.uv]
build-constraint-dependencies = [
    { requirement = "setuptools==68.2.2", hashes = ["sha256:b454a35605876da60632df1a60f736524eb73cc47bbc9f3f1ef1b644de74fd2a"] },
    "wheel<1",
]
```

Set `require-build-hashes = true` under `[tool.uv]` (or pass the flag) to require a hash for every build dependency; each must then be pinned exactly (or a direct URL) with a hash. Hashes can also come from URL fragments in `build-system.requires`.

- Block accidental uploads to PyPI:

```toml
[project]
classifiers = ["Private :: Do Not Upload"]
```

PyPI then rejects the upload; other registries are unaffected. Also use per-project PyPI API tokens, so a token matching the project must exist to publish.

## Gotchas

- `--require-build-hashes` is experimental; `--preview-features build-dependency-hashes` suppresses the warning.
- With build isolation disabled, uv uses installed build dependencies without hash checks, and does not recheck installed packages or previously built wheels. The bundled `uv_build` backend needs no hash.
- Hashes cannot come from requirements returned by a build backend.

## Verify

After `uv build`, `ls dist/` shows the `.whl` and `.tar.gz` files.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/build). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
