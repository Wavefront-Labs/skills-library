---
id: computing-software.software-engineering.uv.uv-add-remove-dependencies
name: uv-add-remove-dependencies
category: computing-software
field: software-engineering
product: uv
tags: [uv, uv-add, uv-remove, project-dependencies, requirements, specifiers, markers, python]
level: practitioner
status: docs-checked
description: "Add, change, remove and import project dependencies with uv add and uv remove, including version specifiers and platform-specific environment markers."
sources: [https://docs.astral.sh/uv/concepts/projects/dependencies/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adding and removing dependencies with uv

Goal: edit `project.dependencies` through uv, with correct specifiers and markers.

## Method

- Add: `uv add httpx` writes e.g. `dependencies = ["httpx>=0.27.2"]`. The bound style is set by `--bounds` (setting `add-bounds`); or give the constraint directly: `uv add "httpx>=0.20"`.
- Other tables: `--dev`, `--group <name>` or `--optional <extra>` add to another field; the same flags work with `uv remove`.
- Change a constraint by re-adding: `uv add "httpx>0.1.0"`. The locked version only changes if the new constraint excludes it; to force the newest allowed version add `--upgrade-package httpx`.
- Remove: `uv remove httpx`. A matching `tool.uv.sources` entry is also removed if nothing else references the dependency.
- Import: `uv add -r requirements.txt`.
- Non-registry source: `uv add "httpx @ git+https://github.com/encode/httpx"` writes the bare name in `dependencies` plus a `[tool.uv.sources]` entry. `uv add "httpx @ ../httpx"` switches to a local path.
- Unsatisfiable input (for example `uv add "httpx>9999"`) fails with "No solution found when resolving dependencies".
- Platform-specific: `uv add "jax; sys_platform == 'linux'"` or `uv add "numpy; python_version >= '3.11'"` store the marker in `dependencies`.

## Specifier syntax (PEP 508)

Order: name, extras, version specifier, marker. Examples from the docs:

- `foo >=1.2.3,<2,!=1.4.0` (comma = AND)
- `foo ==2` matches 2.0.0; `foo ==2.1.*` any 2.1 release
- `foo ~=1.2` is `>=1.2,<2`; `foo ~=1.2.3` is `>=1.2.3,<1.3`
- `pandas[excel,plot] ==2.2`
- `colorama >=0.4.6,<5; platform_system == "Windows"`
- combine markers with `and`, `or`, parentheses.

## Gotchas

- Versions inside markers must be quoted; versions outside markers must not be.
- `project.dependencies` is what is used when uploading to PyPI or building a wheel.
- Editing `pyproject.toml` directly is equally valid.

## Verify

After `uv add httpx`, `pyproject.toml` shows `httpx>=` in `dependencies`. `uv add "httpx>9999"` produces the "No solution found" error.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/dependencies). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
