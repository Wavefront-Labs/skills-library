---
id: computing-software.software-engineering.uv.uv-entry-points-packaging
name: uv-entry-points-packaging
category: computing-software
field: software-engineering
product: uv
tags: [uv, entry-points, requires-python, build-system, package-false, project-scripts, venv-path, python]
level: practitioner
status: docs-checked
description: "Configure a uv project: requires-python, project.scripts and plugin entry points, when a build system is needed, tool.uv.package, and the environment path."
sources: [https://docs.astral.sh/uv/concepts/projects/config/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entry points, build systems and packaging in uv

Goal: decide whether the project is a package and declare its commands correctly.

## Method

- `project.requires-python` (recommended, e.g. `">=3.12"`) sets the allowed syntax and limits dependency versions to those supporting the same range.
- Entry points need a build system defined. CLI: `[project.scripts]` with `hello = "example:hello"`, run with `uv run hello`. GUI: `[project.gui-scripts]` with `hello = "example:app"`; differs only on Windows, where it is wrapped in a GUI executable. Plugins: `[project.entry-points.'example.plugins']` with `a = "example_plugin_a"`, loaded by `importlib.metadata.entry_points(group="example.plugins")` then `plugin.load()`. The group key is arbitrary; namespace it by package name.
- Build system: a `[build-system]` table makes uv build and install the project into the environment; without one it installs only the dependencies. `uv init` defaults to the uv build backend; `--build-backend` picks another, `--no-package` creates a flat unpackaged project.
- You probably need a package for commands, distribution, `src`/`test` layout or a library. You probably do not for scripts, simple applications or a flat layout.
- Override with `tool.uv.package`: `true` forces build and install (legacy setuptools backend if no build system); `false` ignores the declared build system, though an explicit `uv build` still works.
- Environment path: `UV_PROJECT_ENVIRONMENT` replaces `.venv`. A relative path resolves against the workspace root; an absolute path is used as is; uv creates the environment if absent.
- `uv sync` and `uv run` accept `--no-editable` (editable is default), intended for deployment such as a Docker image.

## Gotchas

- If no build system is declared for a dependency package, `setuptools.build_meta:__legacy__` is used; local path dependencies and `uv pip` installs are built regardless.
- `UV_PROJECT_ENVIRONMENT` pointing at the system prefix (for example `/usr/local`) is not recommended: `uv sync` removes extraneous packages and may break the system. An absolute path shared across projects is overwritten by each; use for a single project in CI or Docker.
- uv ignores `VIRTUAL_ENV` for project operations and warns on mismatch. `--active` opts in; `--no-active` silences the warning.

## Verify

With `hello = "example:hello"` under `[project.scripts]` and a build system present, `uv run hello` runs the function.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/config). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
