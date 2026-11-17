---
id: computing-software.software-engineering.uv.uv-build-backend-usage
name: uv-build-backend-usage
category: computing-software
field: software-engineering
product: uv
tags: [uv, build-backend, uv-build-backend, build-system, namespace-packages, stub-packages, module-name]
level: practitioner
status: docs-checked
description: "Choose and configure the uv_build backend: build-system setup, module-name and module-root, namespace packages, and -stubs type stub packages."
sources: [https://docs.astral.sh/uv/concepts/build-backend/, https://docs.astral.sh/uv/concepts/projects/build/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Using the uv_build backend

Goal: build a pure Python package with uv's native backend and lay out modules so it finds them.

## Method

Choose it for most pure Python projects: near zero configuration, validates metadata and structure, fast. It supports only pure Python code; use another backend for extension modules, and consider hatchling when you need build scripts or a more flexible layout.

Enable it (or let `uv init` do so), with an upper bound because it follows uv's versioning policy:

```toml
[build-system]
requires = ["uv_build>=0.13.7,<0.14"]
build-backend = "uv_build"
```

`uv build` uses the copy bundled in the uv executable if its version satisfies the requirement, otherwise a compatible `uv_build` package. Frontends such as `python -m build` always use the `uv_build` package.

Modules: by default one root module is expected at `src/<package_name>/__init__.py`. The name is normalized: lowercased, dots and dashes become underscores (`Foo-Bar` gives `foo_bar`). Override with settings under `[tool.uv.build-backend]`:

```toml
[tool.uv.build-backend]
module-name = "FOO"
module-root = ""
```

That layout is `FOO/__init__.py` beside pyproject.toml.

Namespace packages (a `.` in `module-name`): for `src/foo/bar/__init__.py` set `module-name = "foo.bar"`; `foo` gets no `__init__.py`. Several roots, not recommended (a workspace is preferred): `module-name = ["foo", "bar"]`. For many modules: `namespace = true`, or with a declared root `module-name = "foo"` plus `namespace = true` (recommended for `src/foo/bar` and `src/foo/baz`).

Stub packages: the module name ends in `-stubs` (not normalized to an underscore) and uv looks for `__init__.pyi`, e.g. `src/foo-stubs/__init__.pyi`. Stubs also work with namespace packages.

## Gotchas

- `namespace = true` disables safety checks; prefer an explicit list of module names outside legacy projects.
- Through non-uv frontends, debug with `RUST_LOG=uv=debug` or `RUST_LOG=uv=verbose`.

## Verify

Run `uv build`; the backend creates the sdist and wheel in `dist/`.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/build-backend; concepts/projects/build). Removed or changed: added the projects/build page to sources (it is where the dist/ claim comes from).

Method: documentation only; no commands were run.
