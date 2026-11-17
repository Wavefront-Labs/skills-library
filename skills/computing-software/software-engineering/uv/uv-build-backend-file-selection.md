---
id: computing-software.software-engineering.uv.uv-build-backend-file-selection
name: uv-build-backend-file-selection
category: computing-software
field: software-engineering
product: uv
tags: [uv, build-backend, uv-build-backend, source-include, source-exclude, wheel-exclude, data-directories]
level: advanced
status: docs-checked
description: "Control which files uv_build packs into sdists and wheels with source-include, source-exclude, wheel-exclude, data directories and anchored glob syntax."
sources: [https://docs.astral.sh/uv/concepts/build-backend/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File inclusion and exclusion in uv_build

Goal: predict and adjust what ends up in the source distribution and wheel. Settings live under `[tool.uv.build-backend]`.

## Method

Rule: uv adds included files, then removes excluded ones, so exclusions always win. Defaults exclude `__pycache__`, `*.pyc` and `*.pyo`.

Source distribution contains:

- `pyproject.toml` rewritten in TOML 1.0-compatible syntax, plus the original as `pyproject.toml.orig`.
- The module under `module-root`.
- Files referenced by `project.license-files` and `project.readme`.
- All directories under `data`.
- Files matching `source-include`.

Then `source-exclude` and the default excludes are removed.

Wheel contains:

- The module under `module-root`.
- `project.license-files` (copied into `.dist-info`).
- `project.readme` (copied into the metadata).
- Directories under `data` (copied into the `.data` directory).

Then `source-exclude`, `wheel-exclude` and the default excludes are removed. Source excludes also apply to wheels so a wheel built from the source tree matches one built from the sdist.

There are no wheel includes. A wheel needs exactly one top-level module, and data files must be under the module root or in a `data` directory (small data normally sits in the module root).

Pattern syntax (reduced portable glob from PEP 639, plus backslash escaping):

- Includes are anchored: `pyproject.toml` matches only the root file. Use `/**` for recursion, e.g. `src/**`; `assets/**/sample.csv` matches every `sample.csv` under the root `assets`.
- Avoid unanchored include patterns such as `**/sample.csv` (performance and reproducibility).
- Excludes are not anchored: `__pycache__` removes every directory of that name, with all children. Prefix `/` to anchor, e.g. `/dist` removes only the root `dist`.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/build-backend). Removed or changed: removed the Gotchas and Verify sections (an unconfirmed claim and an invented Verify step).

Method: documentation only; no commands were run.
