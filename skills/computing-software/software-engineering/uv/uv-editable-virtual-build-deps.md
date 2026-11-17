---
id: computing-software.software-engineering.uv.uv-editable-virtual-build-deps
name: uv-editable-virtual-build-deps
category: computing-software
field: software-engineering
product: uv
tags: [uv, editable, virtual-dependencies, build-dependencies, build-system, package-false, no-sources, python]
level: practitioner
status: docs-checked
description: "Control whether a uv dependency is installed editable, treated as virtual (package = false), and how build-system.requires interacts with tool.uv.sources."
sources: [https://docs.astral.sh/uv/concepts/projects/dependencies/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Editable, virtual and build dependencies

Goal: choose how a local dependency is installed and how its build requirements resolve.

## Editable

A normal directory install builds a wheel and copies sources, so edits go stale. An editable install adds a `.pth` link so the interpreter uses the source directly. Limits: the build backend must support it, and native modules are not recompiled before import. Workspace packages are editable by default.

- `uv add --editable ./path/foo` (writes `editable = true`)
- `uv add --no-editable ./path/foo` opts out.
- Path dependencies are not editable by default.

## Virtual

A virtual dependency is not installed as a package but its own dependencies are. Dependencies are never virtual by default. A `path` or `workspace` source is treated as a package (and built, even with no build system) unless it sets `tool.uv.package = false`.

```toml
[tool.uv.sources]
bar = { path = "../projects/bar", package = false }
```

- `package = true` on the source overrides a dependency that sets `tool.uv.package = false`.
- A workspace member that is not depended on, and has no build system, is virtual by default: it is not installed but its dependencies (e.g. `anyio`) are. If the parent depends on it with `child = { workspace = true }`, it is built and installed.

## Build dependencies

For a packaged project, build requirements go in `[build-system] requires` (PEP 518), for example `requires = ["setuptools>=42"]` with `build-backend = "setuptools.build_meta"`. uv respects `tool.uv.sources` for them, so `setuptools = { path = "./packages/setuptools" }` builds with a local copy.

## Gotchas

- Other build tools such as `pypa/build` ignore `tool.uv.sources`. Before publishing run `uv build --no-sources` to confirm the package builds without them.

## Verify

`uv build --no-sources` succeeds for the project.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/dependencies). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
