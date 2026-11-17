---
id: computing-software.software-engineering.uv.uv-init-project-kinds
name: uv-init-project-kinds
category: computing-software
field: software-engineering
product: uv
tags: [uv, uv-init, app-lib-package, project-init, build-backend, src-layout, python]
level: practitioner
status: docs-checked
description: "Choose the right uv init flags for an application, library, extension-module, unpackaged or bare project and know what files each creates."
sources: [https://docs.astral.sh/uv/concepts/projects/init/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating projects with uv init

Goal: pick the `uv init` template that matches the project and know what it generates.

## Method

`uv init` creates a project in the working directory; `uv init foo` uses a target directory (`--directory` changes the base the path is relative to). It exits with an error if the target already has a `pyproject.toml`.

| Need | Command | Result |
|---|---|---|
| Application (default) | `uv init example-app` (or `--app`) | `src/example_app/__init__.py`, `.python-version`, `README.md`, `pyproject.toml`; a `[project.scripts]` entry `example-app = "example_app:main"` |
| Library | `uv init --lib example-lib` | same `src` layout plus a `py.typed` marker; always a packaged project |
| Other build backend | `--build-backend` with `hatchling`, `uv_build`, `flit-core`, `pdm-backend`, `setuptools`, `maturin` or `scikit-build-core` | implies `--package` |
| Extension module | `uv init --build-backend maturin example-ext` (Rust) or `scikit-build-core` (C, C++, FORTRAN, Cython) | maturin adds `Cargo.toml` and `src/lib.rs`; scikit-build-core adds CMake config and `main.cpp` |
| No build system | `uv init --no-package example-app` | `main.py`, `.python-version`, `README.md`, `pyproject.toml`; not installed into the environment |
| Only a `pyproject.toml` | `uv init example-bare --bare` | no pin file, README, sources, git init, description or authors |

Default packaged projects use the `uv_build` backend, for example `requires = ["uv_build>=0.13.7,<0.14"]` and `build-backend = "uv_build"`. Before v0.12 applications had no build system by default.

`--bare` combines with `--lib` or `--build-backend` (build system configured, no file structure). Opt-in extras: `uv init example-bare --bare --description "Hello world" --author-from git --vcs git --pin-python`.

## Gotchas

- With maturin or scikit-build-core, uv sets `tool.uv.cache-keys` to common source file types. To force a rebuild after changes outside those keys, use `--reinstall`.
- `src` layout keeps library code isolated from `python` invocations in the project root.

## Verify

From the generated app: `cd example-app && uv run example-app` prints `Hello from example-app!`. For a library: `uv run python -c "import example_lib; print(example_lib.hello())"` prints `Hello from example-lib!`.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/init). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
